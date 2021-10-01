from flask import Flask, render_template, abort

from .config import config
from .forms import DynamicFormGenerator

app = Flask(__name__)


@app.context_processor
def register_project():
    return {
        "project": config.get("repo", "name"),
    }



@app.route("/<path:key>/", methods=["GET", "POST"])
def issue_form(key: str):
    form = DynamicFormGenerator(key, meta={"csrf": False})
    if not form:
        abort(404)

    return render_template(
        "issue.html",
        title=form.get_meta("title"),
        description=form.get_meta("description"),
        fullwidth=form.get_meta("fullwidth"),
        hide_title=form.get_meta("hide_title"),
        form=form,
        )
