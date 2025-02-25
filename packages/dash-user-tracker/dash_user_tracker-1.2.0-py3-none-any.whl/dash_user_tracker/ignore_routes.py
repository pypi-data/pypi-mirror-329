import inspect
import os

from dash import Dash, callback, get_app
from dash._callback import GLOBAL_CALLBACK_MAP
from werkzeug.routing import Map, MapAdapter, Rule

DASH_PUBLIC_ASSETS_EXTENSIONS = "js,css,png,jpg,jpeg,svg,gif,ico"
BASE_IGNORE_ROUTES = [
    f"/assets/<path:path>.{ext}"
    for ext in os.getenv(
        "DASH_PUBLIC_ASSETS_EXTENSIONS",
        DASH_PUBLIC_ASSETS_EXTENSIONS,
    ).split(",")
] + [
    "/_dash-component-suites/<path:path>",
    "/_dash-layout",
    "/_dash-dependencies",
    "/_favicon.ico",
    "/_reload-hash",
]
IGNORE_ROUTES = "IGNORE_ROUTES"
IGNORE_CALLBACKS = "IGNORE_CALLBACKS"

def add_ignore_routes(app: Dash, routes: list):
    """Add routes to the ignore routes list.

    The routes passed should follow the Flask route syntax.
    e.g. "/admin", "user/<user_id>", etc.

    Some routes are made available by default:
    * All dash scripts (_dash-dependencies, _dash-components-suites/**)
    * All dash mechanics routes (_dash-layout, _reload-hash)
    * All assets with extension .css, .js, .svg, .png, .jpg, .jpeg, .gif, .ico
        Note: You can modify the extension by setting the
        DASH_PUBLIC_ASSETS_EXTENSIONS environment variable.
    * The favicon route (_favicon.ico)

    f you use callbacks on your ignore routes, you should use tracker's
    `ignore_callback` decorator to prevent tracking on those routes.

    Args:
        app (Dash): The Dash app instance.
        routes (list): A list of routes to ignore.
    """
    ignore_routes = get_ignore_routes(app)

    if not ignore_routes.map._rules:
        routes = BASE_IGNORE_ROUTES + routes

    for route in routes:
        ignore_routes.map.add(Rule(route))

    app.server.config[IGNORE_ROUTES] = ignore_routes

def ignore_callback(*callback_args, **callback_kwargs):
    """Ignore a callback from being tracked.

    This works by adding the callback id (from the callback map)  to a list
    of whitelisted callbacks in the Flaks server's config.

    Args:
        *callback_args: The callback arguments.
        **callback_kwargs: The callback keyword arguments.
    """
    def decorator(func):
        wrapped_func = callback(*callback_args, **callback_kwargs)(func)
        callback_id = next(
            (
                k for k, v in GLOBAL_CALLBACK_MAP.items()
                if inspect.getsource(v["callback"]) == inspect.getsource(func)
            ),
            None,
        )
        try:
            app = get_app()
            app.server.config[IGNORE_CALLBACKS].append(callback_id)
        except Exception:
            print(
                "Could not setup the ignore callback as the Dash object "
                "has not yet been instantiated."
            )

        def wrap(*args, **kwargs):
            return wrapped_func(*args, **kwargs)

        return wrap

    return decorator

def get_ignore_routes(app: Dash) -> MapAdapter:
    "Retrieve the ignore routes from the Dash app."
    return app.server.config.get(IGNORE_ROUTES, Map([]).bind(""))

def get_ignore_callbacks(app: Dash) -> list:
    """Retrieve the ignore callbacks from the Dash app."""
    return app.server.config.get(IGNORE_CALLBACKS, [])
