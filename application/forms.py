from typing import Union
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from .github.parser import GithubElement, MarkdownGithubElement
from .github.issue import get_issue_form_data
from .config import forms


form_classes = {}


def DynamicFormGenerator(key: str, submit_label: str="Submit", **kwargs) -> Union[tuple, None]:
    form_class = form_classes.get(key, None)
    if form_class: # class already exists
        return form_class(**kwargs)

    section = forms.get(key, None)
    if section is None: # the given key does not exist in the config
        return None

    data = get_issue_form_data(section.get("file"))
    body = data["body"]

    class IssueForm(FlaskForm):
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
    IssueForm.set_meta("title", data["name"])
    IssueForm.set_meta("description", data["description"])
    IssueForm.set_meta("fullwidth", section.getboolean("fullwidth", False))
    IssueForm.set_meta("hide_title", section.getboolean("hide_title", False))

    form_classes[key] = IssueForm

    return IssueForm(**kwargs)
