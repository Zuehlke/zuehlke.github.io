import time

import requests
import re
import log
import util

ORG = 'zuehlke'
BASE_URL = "https://api.github.com"
KEY_VARS = ['name', 'owner', 'html_url', 'created_at', 'updated_at', 'stargazers_count', 'language', 'forks_count']
SUB_KEY_WARS = {'owner': ('login', 'id')}


class GitHubApi:

    def __init__(self, context):
        self._context = context
        self._api_token = context.get_github_token()
        self._default_headers = {
            "Authorization": f"token {context.get_github_token()}"
        }
        self._rate_limit_status = None

    def update_rate_limit_status(self):
        res = requests.get(f"{BASE_URL}/rate_limit", headers=self._default_headers)
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

    def _api_request(self, url, headers=None, expected_status_codes=None, retry=0):
        if headers is None:
            headers = self._default_headers
        if expected_status_codes is None:
            expected_status_codes = [200]

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

        # TODO: If this header is not None, its value is essentially an "ad-hoc rate limit".
        retry_after_header = response.headers.get("Retry-After")
        if retry_after_header is not None:
            log.abort_and_exit("GHUB", f"Found Retry-After header: '{retry_after_header}'.")

        if (status == 403) or (status not in expected_status_codes):
            # Check for rate limiting in case of unexpected status code.
            if self.is_rate_limited():
                # Wait until the rate limit should be lifted.
                self._handle_rate_limit()
            else:
                # It was not a rate limiting issue - log a warning.
                log.warning("GHUB", f"Unexpected status code {status} for request {url}.")

            # Rate limit should now be lifted if there was one. Retry, update number of retries.
            self._api_request(url, headers, expected_status_codes, retry + 1)

        return status, response.json(), self._parse_link_header(response.headers.get("Link"))

    # TODO: Factor out.
    def _collect_repo_page(self, url, repos):
        _, data, cursor = self._api_request(url)
        for repo in data:
            repos[repo['id']] = {k: v for k, v in repo.items() if k in KEY_VARS}
            for sub_key in SUB_KEY_WARS:
                repos[repo['id']][sub_key] = {k: v for k, v in repo[sub_key].items() if k in SUB_KEY_WARS[sub_key]}
        return cursor

    # TODO: Factor out.
    def collect_org_repos(self):
        log.info("GHUB", "Fetching org repos.")
        initial_url = f"{BASE_URL}/orgs/{ORG}/repos"
        repos = {}
        cursor = {
            "next": initial_url
        }
        while cursor["next"] is not None:
            next_url = cursor["next"]
            log.info("GHUB", f"Fetching '{next_url}'.")
            cursor = self._collect_repo_page(next_url, repos)

        log.info("GHUB", "Done fetching org repos.")
        return repos
