from typing import List
from dash import Dash
from werkzeug.routing import MapAdapter
import re

class DashRouter:
    def __init__(self, app: Dash):
        """
        Initialize router with Dash app's base pathname

        Args:
            app (Dash): Dash app instance
        """
        base_path = app.config.get('url_base_pathname', '/')
        if not base_path:
            base_path = '/'

        base_path = base_path.strip('/')
        self.base_pathname = f'/{base_path}/' if base_path else '/'

    def normalize_path(self, path: str) -> str:
        """
        Remove base pathname from the start of the path

        Args:
            path (str): Full path including base pathname

        Returns:
            str: Path without base pathname
        """
        if path.startswith(self.base_pathname):
            normalized = path[len(self.base_pathname):]
            return f"/{normalized}" if normalized else "/"

        return path if path.startswith('/') else f"/{path}"

    def is_dash_callback(self, path: str) -> bool:
        """Check if a path is a Dash callback route.

        Args:
            path (str): The path to check.

        Returns:
            bool: True if the path is a Dash callback route, False otherwise.
        """
        internal_routes = [
            '/_dash-update-component',
        ]
        normalized_path = self.normalize_path(path)
        return any(route == normalized_path or normalized_path.startswith(route)
              for route in internal_routes)

    def match_ignore_routes(self, path: str, ignore_routes: MapAdapter) -> bool:
        """
        Match path againts ignore routes

        Args:
            path (str): Path to match
            ignore_routes (MapAdapter): Routes to ignore

        Returns:
            bool: Whether the path should be ignored
        """
        normalized_path = self.normalize_path(path)
        return ignore_routes.test(normalized_path)
