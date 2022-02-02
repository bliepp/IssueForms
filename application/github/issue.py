from configparser import SectionProxy
import json
import yaml
import requests

from ..config import config
from .parser import *



def get_issue_form_data(FILE_NAME: str, REPO_OWNER: str, REPO_NAME: str, USERNAME: str, PASSWORD: str) -> dict:
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/.github/ISSUE_TEMPLATE/{FILE_NAME}"

    with requests.Session() as session:
        session.auth = (USERNAME, PASSWORD)
        r = session.get(url)
        if r.status_code != 200:
            raise FileNotFoundError(f"\"{FILE_NAME}\" was not found in repo {REPO_OWNER}/{REPO_NAME}")
        src = session.get(json.loads(r.text)["download_url"]).text

    return yaml.load(src, Loader=yaml.SafeLoader)



def add_issue(REPO_OWNER: str, REPO_NAME: str, USERNAME: str, PASSWORD: str, **kwargs) -> None:
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

    with requests.Session() as session:
        session.auth = (USERNAME, PASSWORD)
        r = session.post(url, json.dumps(kwargs))

        if r.status_code == 201:
            print("Success")
            #print(r.text)
        else:
            print(f"Failure: {r.status_code}")
            #print(r.text)
