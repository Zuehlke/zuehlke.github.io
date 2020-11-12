import requests
import pprint
import re

ORG = 'zuehlke'
URL_RE = 'https://[\w_-]+(?:(?:\.[\w_-]+)+)[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-]?'
KEY_VARS = ['name', 'owner', 'html_url', 'created_at', 'updated_at', 'stargazers_count', 'language', 'forks_count']
SUB_KEY_WARS = {'owner': ('login', 'id')}


def get_api_links(org):
    links = [f"https://api.github.com/orgs/{org}/repos"]

    count = 0
    while True:
        cur_links = requests.get(links[count], auth=('chschoenenberger', 'gU/#8At7Ui')).headers['link']
        if not 'rel="next"' in cur_links:
            break
        else:
            next_link = re.findall(URL_RE, cur_links.split('rel="next"')[0])[-1]
            links.append(next_link)
            count += 1

    return links


def get_repos(url):
    repos_json = requests.get(url).json()
    repos = {}

    for repo in repos_json:
        repos[repo['id']] = {k: v for k, v in repo.items() if k in KEY_VARS}
        for sub_key in SUB_KEY_WARS:
            repos[repo['id']][sub_key] = {k: v for k, v in repo[sub_key].items() if k in SUB_KEY_WARS[sub_key]}

    return repos

repos = {}
for url in get_api_links(ORG):
    repos.update(get_repos(url))

pprint.pprint(repos)
print(len(repos))