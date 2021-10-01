# IssueForms
IssueForms is an open source way to expose your issue form templates to users, which don't have a GitHub account.

It allows not only anonymous issue tracking for private and public repositories but also enables form based issue tracking for private repositories, even for the free plan. 

## How it works
1. Run IssueForms on any server that allows you to host WSGI applications
1. IssueForms reads the issue form templates from your github repository and parses them into Flask compatible WTForms.
1. When submitting a form, IssueForms connects to the GitHub API and submits the issue with an account of your choice.

Since the parsing and issue message generation happens inside of IssueForms the repo does not have to be public (even with the free plan).

## Quick setup and initialization
Clone the repository with its dependencies:
```bash
~ $ git clone --recursive git@github.com:bliepp/IssueForms.git
~ $ cd IssueForms
```

Now create a new virtual environment and install the needed python packages.
```bash
IssueForms $ python -m venv .venv
IssueForms $ source .venv/bin/activate
(.venv) IssueForms $ pip install -r requirements.txt
```

The next step is to create and modify the `config.ini`
```bash
(.venv) IssueForms $ cp config_sample.ini config.ini # create config file
(.venv) IssueForms $ nano config.ini # configure Issueforms
```
Now run a development server
```bash
(.venv) IssueForms $ chmod 755 main.py # make it executable
(.venv) IssueForms $ ./main.py
```
**Important: Flask's builtin WSGI server is only for development and testing. For production/deployment use `gunicorn`, `cheroot` or something similar!**

## Notes
* The project depends not only on [Flask](https://flask.palletsprojects.com/en/1.1.x/), but also some Flask plugins (mainly flask-wtf).
* The HTML, CSS and JS part of the program depends on [Bootstrap 5](https://getbootstrap.com/). This is implemented via a CDN, so no direct dependency is needed.
