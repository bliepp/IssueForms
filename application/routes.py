import copy
import wtforms

from application import app
from application.forms import DynamicFormGenerator, select_api, Form
from application.issues import IssueAPI



@app.error(404)
@app.view("404.html")
def error404(error):
    return dict(
        title=f"{error.status_code} - {error.body}",
        hide_title=True,
        fullwidth=True,
    )



@app.get("/thankyou")
@app.view("thankyou.html")
def thankyou():
    return dict(
        title="Thank You",
        hide_title=True,
        fullwidth=True,
    )



@app.get("/<key:path>")
@app.post("/<key:path>")
@app.view("issue.html")
def issue_form(key: str):
    api : IssueAPI = select_api()

    form : Form = DynamicFormGenerator(key, app.request.POST)
    if not form:
        app.abort(404, f"Not found: '/{key}'")


    if app.request.method == "POST" and form.validate():
        fields = copy.deepcopy(form._fields)
        fields.pop("submit") # remove submit button
        form_title = fields.pop("form_title").data

        content = ""
        for key, item in fields.items():
            content += f"### {item.label.text}\n"
            if issubclass(item.field_class, wtforms.fields.SelectFieldBase):
                options = dict(item.choices)
                indices = list(item.data)
                selection = ["* " + options[int(i)] for i in indices]
                content += "\n".join(selection) + "\n"
            if issubclass(item.field_class, wtforms.fields.StringField):
                if render_type:=item.description.get("type"):
                    item.data = "```" + render_type + "\n" + item.data + "\n```"
                content += item.data + "\n"

            content += "\n"

        api.post(
            **form.get_meta("login_credentials"),
            title=form_title,
            body=content,
            labels=form.get_meta("labels")
            )

        app.redirect("thankyou")

    return dict(
        title=form.get_meta("project") + " - " + form.get_meta("title"),
        description=form.get_meta("description"),
        fullwidth=form.get_meta("fullwidth"),
        hide_title=form.get_meta("hide_title"),
        form=form,
        )
