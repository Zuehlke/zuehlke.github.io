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

    def __init__(self, context):
        self._context = context
        self._api_token = context.get_github_token()
        self._rate_limit_status = None

    def update_rate_limit_status(self):
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
        if self._rate_limit_status is None:
            self.update_rate_limit_status()
        max_age_sec = self._context.get_config("rate_limit_max_age_sec")
        return (round(time.time()) - self._rate_limit_status["last_update"]) > max_age_sec

    def request_rate_limit_status(self, force_update=False, ignore_stale=False):
        if self._rate_limit_status is None:
            self.update_rate_limit_status()
        if force_update or (self.is_rate_limit_status_stale() and not ignore_stale):
            self.update_rate_limit_status()
        return self._rate_limit_status

    def is_rate_limited(self, force_update=False, ignore_stale=False):
        status = self.request_rate_limit_status(force_update, ignore_stale)
        return status["remaining"] <= 0

    def _get_authorization_header(self):
        return f"token {self._context.get_github_token()}"

    @staticmethod
    def _parse_rate_limit_headers(headers):
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

    def _handle_rate_limit(self):
        if self.is_rate_limit_status_stale():
            self.update_rate_limit_status()
        sleep_duration = self._rate_limit_status["reset_in_sec"] + self._context.get_config("rate_limit_buffer_sec")
        time.sleep(sleep_duration)
        wakeup_time = util.epoch_to_local_datetime(self._rate_limit_status["reset_at_utc"])
        log.warning("GHUB", f"Rate limit reached - sleeping for {sleep_duration}s until {wakeup_time}.")
        time.sleep(sleep_duration)

    @staticmethod
    def _parse_link_header(link_header):
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

    def get(self, url, authenticate=True, headers=None, query_params=None, expected_status_codes=None, retry=0):
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
        log.info("GHUB", f"Fetching page '{url}'.")
        _, data, cursor = self.get(url, authenticate, headers, query_params, expected_status_codes)
        page = data
        if type(data) is not list:
            page = [data]
        return cursor, page

    def fetch_all_pages(self, initial_url, flatten=False, authenticate=True, headers=None, query_params=None, expected_status_codes=None):
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

    def _preprocess_repos(self, repos_list):
        return [repo for repo in repos_list if not repo["private"]]

    def _get_repo_contributors(self, owner, repo):
        url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"
        return self.fetch_all_pages(url, flatten=True, query_params={"per_page": 100})

    def _get_org_members(self):
        url = f"{BASE_URL}/orgs/{ORG}/members"
        return self.fetch_all_pages(url, flatten=True, query_params={"per_page": 100})

    def _get_org_repos(self):
        url = f"{BASE_URL}/orgs/{ORG}/repos"
        return self.fetch_all_pages(url, flatten=True, query_params={"per_page": 100})

    def collect_org_repos(self):
        log.info("GHUB", "Collecting org repos.")
        raw_repos = self._get_org_repos()
        preprocessed_repos = self._preprocess_repos(raw_repos)
        parsed_repos = json_reducer.reduce(REPOS_SCHEMA, preprocessed_repos)
        result = {}
        for repo in parsed_repos:
            result[repo["id"]] = repo
        return result

    def collect_org_members(self):
        log.info("GHUB", "Collecting org members.")
        member_urls = [member["url"] for member in self._get_org_members()]
        members = {}
        for member_url in member_urls:
            log.info("GHUB", f"Fetching member '{member_url}'.")
            _, member_raw, _ = self.get(member_url)
            member_parsed = json_reducer.reduce(PERSON_SCHEMA, member_raw)
            members[member_parsed["id"]] = member_parsed
        return members
