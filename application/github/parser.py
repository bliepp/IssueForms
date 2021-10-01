# valid keys: https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-githubs-form-schema
from flask_wtf import FlaskForm
from wtforms import Field, SelectField, StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired

from .exceptions import MissingKey, MissingRequiredArgument, UnknownGithubElementType



class GithubElement():
    __element_types = {}


    def __init_subclass__(cls, key: str=None):
        if not key:
            raise MissingKey(cls.__name__)
        cls.__element_types[key] = cls
        return super().__init_subclass__()

    def __new__(cls, type: str = None, **kwargs):
        subclass = cls.__element_types.get(type, None)
        if not subclass:
            raise UnknownGithubElementType(subclass)

        obj = super().__new__(subclass)
        return obj

    def create(self) -> Field:
        pass



class CheckboxesGithubElement(GithubElement, key="checkboxes"):
    pass # for now not implemented



class DropdownGithubElement(GithubElement, key="dropdown"):
    def __init__(self, attributes: dict={}, id: str="", validations: dict={}, **kwargs) -> None:
        super().__init__()
        self.label = attributes.get("label", None)
        self.options = attributes.get("options", None)
        if self.label is None:
            raise MissingRequiredArgument("label")
        if self.options is None:
            raise MissingRequiredArgument("options")
        self.description = attributes.get("description", "")
        self.multiple = attributes.get("multiple", False)

        self.id = id

        self.required = validations.get("required", False)


    def create(self) -> Field:
        kwargs = dict(
            label=self.label + "*"*self.required,
            validators=[DataRequired()]*self.required,
            choices=list(enumerate(self.options)),
        )

        if self.multiple:
            return SelectMultipleField(render_kw={"size": f"{len(self.options)}"}, **kwargs)

        kwargs["choices"] = [("", "---")] + kwargs["choices"]
        return SelectField(**kwargs)




class InputGithubElement(GithubElement, key="input"):
    def __init__(self, attributes: dict={}, id: str="", validations: dict={}, **kwargs) -> None:
        super().__init__()
        self.label = attributes.get("label", None)
        if self.label is None:
            raise MissingRequiredArgument("label")
        self.description = attributes.get("description", "")
        self.placeholder = attributes.get("placeholder", "")
        self.value = attributes.get("value", None)

        self.id = id

        self.required = validations.get("required", False)


    def create(self) -> Field:
        return StringField(
            label=self.label + "*"*self.required,
            description=self.description,
            id=self.id,
            default=self.value,
            )



class MarkdownGithubElement(GithubElement, key="markdown"):
    def __init__(self, attributes: dict={}, **kwargs) -> None:
        super().__init__()
        self.value = attributes.get("value", None)
        if self.value is None:
            raise MissingRequiredArgument("value")


    def create(self) -> Field:
        return ""



class TextareaGithubElement(GithubElement, key="textarea"):
    def __init__(self, attributes: dict={}, id: str="", validations: dict={}, **kwargs) -> None:
        super().__init__()
        self.label = attributes.get("label", None)
        if self.label is None:
            raise MissingRequiredArgument("label")
        self.description = attributes.get("description", "")
        self.placeholder = attributes.get("placeholder", "")
        self.value = attributes.get("value", None)
        self.render = attributes.get("render", None)

        self.id = id

        self.required = validations.get("required", False)


    def create(self) -> Field:
        return TextAreaField(
            label=self.label + "*"*self.required,
            validators=[DataRequired()]*self.required,
            description=self.description,
            id=self.id,
            default=self.value,
            render_kw={"placeholder": self.placeholder}
        )
