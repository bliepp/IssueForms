import json
import yaml
import requests

from ..config import config
from .parser import *



def get_issue_form_data(file_name: str) -> dict:
    USERNAME = config.get("account", "user", fallback=None)
    PASSWORD = config.get("account", "password", fallback=None)

    REPO_OWNER = config.get("repo", "owner", fallback=USERNAME)
    REPO_NAME = config.get("repo", "name", fallback=None)

    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/.github/ISSUE_TEMPLATE/{file_name}"
    r = session.get(url)

    if r.status_code != 200:
        raise FileNotFoundError(f"\"{file_name}\" was not found in repo {REPO_OWNER}/{REPO_NAME}")

    src = session.get(json.loads(r.text)["download_url"]).text

    return yaml.load(src, Loader=yaml.SafeLoader)



def add_issue(**kwargs) -> None:
    USERNAME = config.get("account", "user", fallback=None)
    PASSWORD = config.get("account", "password", fallback=None)

    REPO_OWNER = config.get("repo", "owner", fallback=None)
    REPO_NAME = config.get("repo", "name", fallback=None)


    session = requests.Session()
    session.auth = (USERNAME, PASSWORD)

    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    r = session.post(url, json.dumps(kwargs))

    if r.status_code == 201:
        print("Success")
        print(r.text)
    else:
        print("Failure")
        print(r.text)