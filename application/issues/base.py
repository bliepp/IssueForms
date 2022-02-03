import json, yaml
import requests



class IssueAPI():
    def __init__(self, form_url: str, issues_url: str, get_success_code: int=200, post_success_code: int=201):
        self.__formurl = form_url
        self.__issuesurl = issues_url
        self.__getcode = get_success_code
        self.__postcode = post_success_code


    def get(self, filename: str, owner: str, repo: str, user: str, password: str) -> dict:
        url = self.__formurl.format(REPO_OWNER=owner, REPO_NAME=repo, FILE_NAME=filename)
        with requests.Session() as session:
            session.auth = (user, password)
            r = session.get(url)
            if r.status_code != self.__getcode:
                raise FileNotFoundError(f"\"{filename}\" was not found in repo {owner}/{repo}")
            src = session.get(json.loads(r.text)["download_url"]).text

        return yaml.load(src, Loader=yaml.SafeLoader)


    def post(self, owner: str, repo: str, user: str, password: str, **kwargs) -> None:
        url = self.__issuesurl.format(REPO_OWNER=owner, REPO_NAME=repo)
        with requests.Session() as session:
            session.auth = (user, password)
            r = session.post(url, json.dumps(kwargs))

            if r.status_code != self.__postcode:
                raise Exception(f"Posting new issue in {owner}/{repo} failed")
