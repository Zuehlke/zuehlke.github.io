import time

import requests
import re

import json_reducer
import log
import util

ORG = 'zuehlke'
BASE_URL = "https://api.github.com"

REPOS_SCHEMA = [{
    "id": {},
    "name": {},
    "owner": {
        "login": {},
        "id": {}
    },
    "html_url": {},
    "created_at": {},
    "updated_at": {},
    "stargazers_count": {},
    "watchers_count": {},
    "forks_count": {},
    "fork": {},
    "language": {},
}]

PERSON_SCHEMA = {
    "id": {},
    "login": {},
    "name": {},
    "bio": {},
    "avatar_url": {},
    "html_url": {},
}


class GitHubApi:
    """Provides a wrapper for fetching data from GitHub API."""

    def __init__(self, context):
        """
        Create a new GitHubApi object.
        :param context: application context
        """
        self._context = context
        self._api_token = context.get_github_token()
        self._rate_limit_status = None

    def _get_authorization_header(self):
        """
        Return the correct authorization header value based on the API token provided in the application context.
        :return: authorization header value
        """
        return f"token {self._context.get_github_token()}"

    def _handle_rate_limit(self):
        """
        Sleep until rate limit block is lifted, plus additional time specified in the config file. Update rate limit
        status as needed.
        """
        if self.is_rate_limit_status_stale():
            self.update_rate_limit_status()
        sleep_duration = self._rate_limit_status["reset_in_sec"] + self._context.get_config("rate_limit_buffer_sec")
        time.sleep(sleep_duration)
        wakeup_time = util.epoch_to_local_datetime(self._rate_limit_status["reset_at_utc"])
        log.warning("GHUB", f"Rate limit reached - sleeping for {sleep_duration}s until {wakeup_time}.")
        time.sleep(sleep_duration)

    def _preprocess_repos(self, repos_list):
        """
        Perform generic, predefined set of actions (filter, sort, transform) on a list of repositories.
        :param repos_list: list of raw repositories, as returned by the GitHub API
        :return: preprocesses list of repositories
        """
        return [repo for repo in repos_list if not repo["private"]]

    def _get_repo_contributors(self, owner, repo):
        """
        Fetch list of contributors for a given repository, identified by owner and repo name.
        :param owner: owner of the repository
        :param repo: name of the repository
        :return: list of contributors as returned by the GitHub API
        """
        url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"
        return self.fetch_all_pages(url, flatten=True, query_params={"per_page": 100})

    def _get_org_members(self):
        """
        Fetch list of members of the Zuehlke GitHub organisation.
        :return: list of members of the Zuehlke org as returned by the GitHub API
        """
        url = f"{BASE_URL}/orgs/{ORG}/members"
        return self.fetch_all_pages(url, flatten=True, query_params={"per_page": 100})

    def _get_org_repos(self):
        """
        Fetch list of repositories owned by the Zuehlke GitHub organisation.
        :return: list of repos owned by the Zuehlke org as returned by the GitHub API
        """
        url = f"{BASE_URL}/orgs/{ORG}/repos"
        return self.fetch_all_pages(url, flatten=True, query_params={"per_page": 100})

    @staticmethod
    def _parse_link_header(link_header):
        """
        Parse contents of the Link header into dictionary.
        :param link_header: Link header value, or None
        :return: dictionary containing links for next, last, first and prev; all of which may be None
        """
        result = {
            "next": None,
            "last": None,
            "first": None,
            "prev": None,
        }
        if link_header is None:
            return result

        links = link_header.split(",")
        for link in links:
            parts = link.split(";")
            if len(parts) != 2:
                log.abort_and_exit("GHUB", f"Failed to parse Link header: '{link_header}'.")
            url = parts[0].strip()[1:-1]
            rel = parts[1]
            if re.match('rel="next"', rel.strip()):
                result["next"] = url
            elif re.match('rel="last"', rel.strip()):
                result["last"] = url
            elif re.match('rel="first"', rel.strip()):
                result["first"] = url
            elif re.match('rel="prev"', rel.strip()):
                result["prev"] = url
        return result

    def update_rate_limit_status(self):
        """
        Fetch latest rate limit status and update status information in this object. Uses an API endpoint
        which is itself not rate-limited, and is therefore not affected by any rate limit blocks. Information
        is presented in a pre-defined rate limit status information dictionary format.
        """
        headers = {"Authorization": self._get_authorization_header()}
        res = requests.get(f"{BASE_URL}/rate_limit", headers=headers)
        if res.status_code != 200:
            log.abort_and_exit("GHUB", f"Failed to update rate limit status, status code {res.status_code}.")
        data = res.json()["rate"]
        self._rate_limit_status = {
            "limit": int(data["limit"]),
            "used": int(data["used"]),
            "remaining": int(data["remaining"]),
            "reset_at_utc": int(data["reset"]),
            "reset_in_sec": int(data["reset"] - round(time.time())),
            "last_update": round(time.time())
        }

    def is_rate_limit_status_stale(self):
        """
        Whether the latest rate limit update is older than the maximum allowed age specified in the
        config file.
        :return: True of the current rate limit status information is stale, False else
        """
        if self._rate_limit_status is None:
            self.update_rate_limit_status()
        max_age_sec = self._context.get_config("rate_limit_max_age_sec")
        return (round(time.time()) - self._rate_limit_status["last_update"]) > max_age_sec

    def request_rate_limit_status(self, force_update=False, ignore_stale=False):
        """
        Get current rate limit status information, triggering status update request if the current
        information is stale.
        :param force_update: force status update request (False)
        :param ignore_stale: stale status information does not require a status update request (False)
        :return: current rate limit status information
        """
        if self._rate_limit_status is None:
            self.update_rate_limit_status()
        if force_update or (self.is_rate_limit_status_stale() and not ignore_stale):
            self.update_rate_limit_status()
        return self._rate_limit_status

    def is_rate_limited(self, force_update=False, ignore_stale=False):
        """
        Whether the authenticated user is currently blocked by rate limitation.
        :param force_update: force rate limit status update request (is allowed during rate limit blocks) (False)
        :param ignore_stale: allow using stale rate limit information for answering this query (False)
        :return: True if currently blocked by rate limitation, False else
        """
        status = self.request_rate_limit_status(force_update, ignore_stale)
        return status["remaining"] <= 0

    @staticmethod
    def _parse_rate_limit_headers(headers):
        """
        Extract rate limit response headers from header dictionary and transform information into a
        pre-defined rate limit status information dictionary format.
        :param headers: response headers returned during any request to the GitHub API
        :return: rate limit status information in pre-defined dictionary format
        """
        limit = int(headers["X-RateLimit-Limit"])
        remaining = int(headers["X-RateLimit-Remaining"])
        reset_at_utc = int(headers["X-RateLimit-Reset"])
        return {
            "limit": limit,
            "used": limit - remaining,
            "remaining": remaining,
            "reset_at_utc": reset_at_utc,
            "reset_in_sec": reset_at_utc - round(time.time()),
            "last_update": round(time.time())
        }

    def get(self, url, authenticate=True, headers=None, query_params=None, expected_status_codes=None, retry=0):
        """
        Perform a GET request to the GitHub API. Appropriately handle rate limits. Retry if failed due to rate limiting
        or unexpected response code. Fail if no success after reaching maximum number of retries as specified in the
        config file. Return the status code, response JSON, and cursor object containing next, first, last and prev
        links.
        :param url: request URL, not including query parameters
        :param authenticate: whether this request should include the appropriate Authorization header (True)
        :param headers: additional custom headers (not including Authorization) (None)
        :param query_params: query parameters dictionary (None)
        :param expected_status_codes: list of status codes for which no retry is necessary ([200, 204])
        :param retry: how many retries have already occurred (0)
        :return: status, response_json, cursor
        """

        # Initialize headers if not provided.
        if headers is None:
            headers = {}

        # Set expected status codes to default value if not provided.
        if expected_status_codes is None:
            expected_status_codes = [200, 204]

        # If request is authenticated, add authorization header.
        if authenticate:
            headers["Authorization"] = self._get_authorization_header()

        # Append query params to URL if provided.
        if query_params is not None:
            url = f"{url}?"
            for key, value in query_params.items():
                url = f"{url}{key}={value}&"

        # If max number of retries is exceeded, abort.
        if retry > self._context.get_config("max_retries"):
            log.abort_and_exit("GHUB", f"Request to {url} with headers {headers} failed after {retry} retries.")

        # Sleep before making request to ensure proper delay.
        time.sleep(self._context.get_config("request_delay_sec"))

        # Before making a request, check for rate limiting. Wait if necessary.
        if self.is_rate_limited():
            self._handle_rate_limit()

        # Make request and update rate limit status from response headers.
        response = requests.get(url, headers=headers)
        self._rate_limit_status = self._parse_rate_limit_headers(response.headers)
        status = response.status_code

        retry_after_header = response.headers.get("Retry-After")
        if retry_after_header is not None:
            # Retry-After header found, indicates abuse rate limiting. Discard response, wait and retry.
            retry_sec = int(retry_after_header)
            log.warning("GHUB",
                        f"Received Retry-After (abuse rate limiting), trying again after '{retry_sec}' seconds.")
            self.update_rate_limit_status()
            self.get(url, headers, expected_status_codes, retry + 1)

        if (status == 403) or (status not in expected_status_codes):
            # Check for rate limiting in case of unexpected status code.
            if self.is_rate_limited():
                # Wait until the rate limit should be lifted.
                self._handle_rate_limit()
            else:
                # It was not a rate limiting issue - log a warning.
                log.warning("GHUB", f"Unexpected status code {status} for request {url}.")

            # Rate limit should now be lifted if there was one. Retry, update number of retries.
            self.get(url, headers, expected_status_codes, retry + 1)

        return status, response.json(), self._parse_link_header(response.headers.get("Link"))

    def request_page(self, url, authenticate=True, headers=None, query_params=None, expected_status_codes=None):
        """
        Perform a GET request to a potentially paginated resource in the GitHub API. Return a list containing all
        items on that page, and a cursor object. This method can also be used for non-paginated responses. It returns
        a result list and cursor in any case.
        :param url: request URL
        :param authenticate: whether to provide appropriate Authorization header (True)
        :param headers: custom headers (None)
        :param query_params: query parameters dictionary (None)
        :param expected_status_codes: response codes for which no retry is necessary ([200, 204])
        :return: result_list, cursor
        """
        log.info("GHUB", f"Fetching page '{url}'.")
        _, data, cursor = self.get(url, authenticate, headers, query_params, expected_status_codes)
        page = data
        if type(data) is not list:
            page = [data]
        return cursor, page

    def fetch_all_pages(self, initial_url, flatten=False, authenticate=True, headers=None, query_params=None,
                        expected_status_codes=None):
        """
        Perform a series of GET requests to a potentially paginated resource in the GitHub API and return results as
        a single list.
        :param initial_url: URL of the first page
        :param flatten: whether to flatten the result list. If False, the result list contains an individual child list
        for each page (False)
        :param authenticate: whether to provide appropriate Authorization header (True)
        :param headers: custom headers (None)
        :param query_params: query parameters dictionary (None)
        :param expected_status_codes: response codes for which no retry is necessary ([200, 204])
        :return: list of page results, potentially flattened
        """
        result = []
        url = initial_url
        while url is not None:
            cursor, page = self.request_page(url, authenticate, headers, query_params, expected_status_codes)
            if flatten:
                for element in page:
                    result.append(element)
            else:
                result.append(page)
            url = cursor["next"]
        return result

    def collect_org_repos(self):
        """
        Get and aggregate all public repositories owned by the Zuehlke org.
        :return: id-indexed dictionary containing all aggregated public Zuehlke org repos
        """
        log.info("GHUB", "Collecting org repos.")
        raw_repos = self._get_org_repos()
        preprocessed_repos = self._preprocess_repos(raw_repos)
        parsed_repos = json_reducer.reduce(REPOS_SCHEMA, preprocessed_repos)
        result = []
        for repo in parsed_repos:
            result.append(repo)
        return result

    def collect_org_members(self):
        """
        Get and aggregate all non-concealed members of the Zühlke org.
        :return: id-indexed dictionary containing all aggregated non-concealed members of the Zühlke org.
        """
        log.info("GHUB", "Collecting org members.")
        member_urls = [member["url"] for member in self._get_org_members()]
        members = []
        for member_url in member_urls:
            log.info("GHUB", f"Fetching member '{member_url}'.")
            _, member_raw, _ = self.get(member_url)
            member_parsed = json_reducer.reduce(PERSON_SCHEMA, member_raw)
            members.append(member_parsed)
        return members
