from .application import app
from .forms import DynamicFormGenerator


@app.get("/<key:path>")
@app.post("/<key:path>")
@app.view("issue.html")
def issue_form(key: str):
    form = DynamicFormGenerator(key)
    if not form:
        app.abort(404)

    if app.request.method == "POST" and form.validate():
        print("valdiated")

    return dict(
        title=form.get_meta("title"),
        description=form.get_meta("description"),
        fullwidth=form.get_meta("fullwidth"),
        hide_title=form.get_meta("hide_title"),
        form=form,
        )
