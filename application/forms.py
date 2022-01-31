import configparser
from typing import Union
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

from .github.parser import GithubElement, MarkdownGithubElement
from .github.issue import get_issue_form_data
from .config import config, form_sections


__form_classes = {}


def DynamicFormGenerator(key: str, *args, submit_label: str="Submit", **kwargs) -> Union[tuple, None]:
    form_class = __form_classes.get(key, None)
    if form_class: # class already exists
        return form_class(*args, **kwargs)

    section:configparser.SectionProxy = form_sections.get(key, None)
    if section is None: # the given key does not exist in the config
        return None

    login_credentials = {}
    login_credentials["FILE_NAME"] = section.get("file", fallback=None)
    login_credentials["USERNAME"] = config.get("account", "user", fallback=None)
    login_credentials["PASSWORD"] = config.get("account", "password", fallback=None)
    login_credentials["REPO_OWNER"] = section.get("repo_owner", fallback=config.get("repo", "owner", fallback=login_credentials["USERNAME"]))
    login_credentials["REPO_NAME"] = section.get("repo_name", fallback=config.get("repo", "name", fallback=None))

    data = get_issue_form_data(**login_credentials)
    body = data.get("body", [])

    class IssueForm(Form):
        __meta_data = {}
        form_title = StringField("Title*", default=data["title"], validators=[DataRequired()], render_kw={
            "autofocus": "autofocus",
            "onfocus": "var tmp = this.value; this.value = ''; this.value = tmp;"})

        @classmethod
        def set_meta(cls, key: str, value):
            cls.__meta_data[key] = value

        @classmethod
        def get_meta(cls, key: str):
            return cls.__meta_data.get(key, None)

    for _ in body:
        element = GithubElement(**_)
        if isinstance(element, MarkdownGithubElement): continue
        setattr(IssueForm, element.id, element.create())

    submit_label = section.get("submit_text", submit_label)

    setattr(IssueForm, "submit", SubmitField(submit_label))
    IssueForm.set_meta("project", section.get(
        "project",
        fallback=section.get(
            "repo_name",
            fallback=config.get("repo", "name", fallback=None))
            )
        )
    IssueForm.set_meta("title", data["name"])
    IssueForm.set_meta("labels", data.get("labels", []))
    IssueForm.set_meta("description", data["description"])
    IssueForm.set_meta("fullwidth", section.getboolean("fullwidth", False))
    IssueForm.set_meta("hide_title", section.getboolean("hide_title", False))
    IssueForm.set_meta("login_credentials", login_credentials)

    __form_classes[key] = IssueForm

    return IssueForm(*args, **kwargs)
