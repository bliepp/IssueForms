import bottle
from .config import config


class Application(bottle.Bottle):
    def __init__(self, *args, **kwargs):
        # bottle setup
        bottle.TEMPLATE_PATH.insert(0, "application/views")

        # renaming and convenience stuff
        self.template = bottle.jinja2_template
        self.view = bottle.jinja2_view
        self.abort = bottle.abort
        self.redirect = bottle.redirect
        self.request = bottle.request

        # initialize
        super().__init__(*args, **kwargs)


app = Application()


@app.hook('before_request')
def strip_path():
    # remove trailing slash
    app.request.environ['PATH_INFO'] = app.request.environ['PATH_INFO'].rstrip('/')
