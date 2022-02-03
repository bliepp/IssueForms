from typing import Union
from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired

from .issues import IssueAPI, GithubIssueAPI
from .parser import ParserElement, MarkdownElement
from .config import config, form_sections, SectionProxy



__form_cache = {}
__api_map = {
    "github": GithubIssueAPI,
}



def select_api(*args, **kwargs) -> IssueAPI:
    # this might be useful if some additional apis re getting added, e.g. GitLab or Gitea
    platform = config.get("account", "platform", fallback="github")
    IssueClass = __api_map.get(platform)
    return IssueClass(*args, **kwargs)



def DynamicFormGenerator(key: str, *args, submit_label: str="Submit", **kwargs) -> Union[tuple, None]:
    # look in cache if form already exists
    FormClass = __form_cache.get(key, None)
    if FormClass: # class already exists
        return FormClass(*args, **kwargs)

    # get section of config matching the key
    section : SectionProxy = form_sections.get(key, fallback=None)
    if section is None: # the given key does not exist in the config
        return None

    # load login credentials from config
    login_credentials = {}
    login_credentials["filename"] = section.get("file", fallback=None)
    login_credentials["user"] = config.get("account", "user", fallback=None)
    login_credentials["password"] = config.get("account", "password", fallback=None)
    login_credentials["owner"] = section.get(
        "repo_owner",
        fallback=config.get(
            "repo",
            "owner",
            fallback=login_credentials["user"]
            )
        )
    login_credentials["repo"] = section.get(
        "repo_name",
        fallback=config.get(
            "repo",
            "name",
            fallback=None
            )
        )

    # get issue form data
    data = select_api().get(**login_credentials)
    body = data.get("body", [])


    # boilerplate class that gets customized
    class IssueForm(Form):
        __meta_data = {}
        form_title = StringField("Title*", default=data["title"], validators=[DataRequired()], render_kw={
            "autofocus": "autofocus",
            "onfocus": "var tmp = this.value; this.value = ''; this.value = tmp;"}) # used to place cursor behind text

        @classmethod # needed to store additional data
        def set_meta(cls, key: str, value):
            cls.__meta_data[key] = value

        @classmethod
        def get_meta(cls, key: str):
            return cls.__meta_data.get(key, None)


    # add fields to form
    for _ in body:
        element = ParserElement(**_)
        if isinstance(element, MarkdownElement): continue
        setattr(IssueForm, element.id, element.create())

    submit_label = section.get("submit_text", submit_label)
    setattr(IssueForm, "submit", SubmitField(submit_label))

    # add additional data to form
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

    # save in cache and return instance
    __form_cache[key] = IssueForm
    return IssueForm(*args, **kwargs)
