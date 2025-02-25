import asyncio
import json
import os
import secrets
from datetime import datetime, timezone
from typing import Optional

from dash import Dash
from flask import request, session

from .http_repository import HttpTrackerRepository
from .ignore_routes import (add_ignore_routes, get_ignore_callbacks,
                            get_ignore_routes)
from .repository import TrackerRepository
from .routers import DashRouter


class Tracker:
    def __init__(
        self,
        app: Dash,
        app_name: Optional[str] = None,
        tracker_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        ignore_routes: Optional[list] = None,
        user_provider: Optional[callable] = None,
        repository: Optional[TrackerRepository] = None,
        enable_page_view_tracking: Optional[bool] = True,
        enable_page_interaction_tracking: Optional[bool] = False,
    ) -> None:
        """Tracker class for tracking Dash app usage.

        Add this class to your Dash app to track page views and
        navigation events.

        The information is sent to a tracker endpoint (Separate
        server) or printed to console.

        The user information is obtained from the Flask session.
        It defaults to anonymous if the session is not available.
        The tracker will try to pull the `user` key from the session
        and extract the `id`, `email`, and `full_name`.

        Args:
            app (Dash): Dash app
            tracker_endpoint (Optional[str], optional): string endpoint
                for tracking, if not supplied, actions will be printed
                to console. Defaults to None.
            api_key (Optional[str], optional): API key for tracking server.
                Defaults to None.
            ignore_routes (Optional[list], optional): list of routes
                to ignore. Defaults to None.
            user_provider (Optional[callable], optional): A callable that
                returns a dictionary of user information. Defaults to None.
            repository (Optional[TrackerRepository], optional): A repository
                for tracking navigation data. Defaults to None.
            enable_page_view_tracking (Optional[bool], optional): Enable
                page view tracking. Defaults to True.
            enable_page_interaction_tracking (Optional[bool], optional): Enable
                page interaction tracking. Defaults to False.
        """
        if os.environ.get("DASH_TRACKER_INITIALIZED"):
            return
        os.environ["DASH_TRACKER_INITIALIZED"] = "1"

        self.app = app
        self.router = DashRouter(app)
        self.app_name = app_name or "Generic Dash App"
        self.tracker_endpoint = tracker_endpoint
        self.api_key = api_key

        self._should_print = False
        self._user_provider = user_provider or self._extract_user_info

        self.analytics = None
        self.repository = repository

        self.enable_page_view_tracking = enable_page_view_tracking
        self.enable_page_interaction_tracking = enable_page_interaction_tracking

        self._set_base_ignore_routes()
        self._setup_tracking()

        if ignore_routes is not None:
            add_ignore_routes(app, ignore_routes)

    def _send_event_sync(self, event_type: str, event_data: dict) -> None:
        """
        Internal synchronous wrapper for sending events in Flask requests context.
        Creates and manages an event loop for sending async events from sync code.
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self._send_event(event_type, event_data))
        finally:
            loop.close()

    async def _send_event(self, event_type: str, event_data: dict) -> None:
        """
        Send event to tracker endpoint or print to console.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        event = {
            "event": event_type,
            "data": event_data,
            "timestamp": timestamp
        }
        if self._should_print:
            print(json.dumps(event))
        elif self.repository:
            try:
                await self.repository.save_event(event)
            except Exception as e:
                print(f"Error sending event to tracker: {e}")
        else:
            print("Warning: No repository supplied and printing is disabled.")


    def _set_base_ignore_routes(self) -> None:
        """Set the base ignore routes for the tracker."""
        add_ignore_routes(self.app, routes = [])


    def set_user_provider(self, user_provider: callable) -> None:
        """Set a custom user provider for the tracker.

        Args:
            user_provider (callable): A callable that returns a dictionary
                of user information.
        """
        self._user_provider = user_provider


    def _extract_user_info(self) -> dict:
        """
        Extract user information from the Flask session.
        It defaults to anonymous if the session is not available.
        """
        user_info = {"user_id": "anonymous", "email": "anonymous", "full_name": "anonymous"}
        if "user" in session:
            user_info["user_id"] = session["user"].get("id", "anonymous")
            user_info["email"] = session["user"].get("email", "anonymous")
            user_info["full_name"] = session["user"].get("full_name", "anonymous")
        return user_info


    def _build_event_data(self, user_info: dict, path: Optional[str] = None) -> dict:
        """
        Build event data for tracking.

        Args:
            user_info (dict): User information
            path (Optional[str], optional): Path to track. Defaults to None.
        """
        return {
            "app_name": self.app_name,
            "ip": request.remote_addr,
            "user_agent": request.user_agent.string,
            "base_url": request.base_url,
            "url": request.url,
            "url_root": request.url_root,
            "referrer": request.referrer,
            "path": path or request.path,
            "full_path": request.full_path,
            "endpoint": request.endpoint,
            "method": request.method,
            **user_info,
        }

    # #################################### #
    #       Specific Tracking Events       #
    # #################################### #
    def _track_page_view(self) -> None:
        """
        Track page view and navigation events.

        The tracker will send a page view event if either
            * The app recognizes a HTTP request (initial page load and API calls)
            * The app recognizes Dash callbacks (to track internal navigation)
        """
        server = self.app.server

        ignore_routes = get_ignore_routes(self.app)
        ignore_callbacks = get_ignore_callbacks(self.app)

        @server.before_request
        def before_request_page_track() -> None:

            # Track Full Page Loads & API Requests
            user_info = self._user_provider()
            event_data = self._build_event_data(user_info)

            # Fallback for Internal Navigation (if `dcc.Location` isn't used)
            if self.router.is_dash_callback(request.path):
                body = request.get_json()

                # Exit early if the request body is not valid
                if not body or "inputs" not in body or "output" not in body:
                    return None

                if body["output"] in ignore_callbacks:
                    return None

                # Check whether the callback has an input using the pathname
                # If it does, check whether the pathname matches a route to ignore.
                pathname = next(
                    (
                        inp.get("value") for inp in body["inputs"]
                        if isinstance(inp, dict)
                        and inp.get("property") == "pathname"
                    ),
                    None,
                )

                if not pathname or self.router.match_ignore_routes(pathname, ignore_routes):
                    return None

                # Check if the path should be tracked to avoid duplicate tracking for _dash-update-component
                # internal navigation.
                if not self._should_track_path(pathname):
                    return None

                event_data["path"] = pathname

            else:
                # If the route is not a callback route, check whether the path
                # matches a route to ignore.
                if self.router.match_ignore_routes(request.path, ignore_routes):
                    return None

                if not self._should_track_path(request.path):
                    return None

            self._send_event_sync("page_view", event_data)
            return None

    def _track_page_interaction(self) -> None:
        """
        Track user interaction within the app

        The tracker will send an interaction event if the app recognizes
        a Dash callback that is not ignored.
        """
        server = self.app.server

        ignore_routes = get_ignore_routes(self.app)
        ignore_callbacks = get_ignore_callbacks(self.app)

        @server.before_request
        def before_request_interaction_track() -> None:
            # Ignore routes that are defined by the user
            if self.router.match_ignore_routes(request.path, ignore_routes):
                    return None
            # Filter out non-Dash callbacks
            if not self.router.is_dash_callback(request.path):
                return None

            body = request.get_json()

            # Exit early if the request body is not valid
            if not body or "inputs" not in body or "output" not in body:
                return None

            # Exit early if the callback is ignored
            if body["output"] in ignore_callbacks:
                return None

            user_info = self._user_provider()
            event_data = self._build_event_data(user_info)

            event_data.update(
                {
                    "interaction": {
                        "changed_props": body.get("changedPropIds", []),
                        "inputs": body.get("inputs", []),
                        "output": body.get("output", []),
                        "outputs": body.get("outputs", []),
                        "state": body.get("state", []),
                    }
                }
            )
            self._send_event_sync("page_interaction", event_data)
            return None

    # #################################### #
    #          General All Events          #
    # #################################### #
    def _track_all_events(self) -> None:
        """
        Combined Tracking method for both page views and page interactions.
        Handles both types of events through a single request handler
        for better performance.

        The tracker will send a page view event if either
            * The app recognizes a HTTP request (initial page load and API calls)
            * The app recognizes Dash callbacks (to track internal navigation)

        The tracker will send a page interaction event if the app recognizes
            * The app recognizes Dash callbacks (to track user interactions)
        """
        server = self.app.server
        ignore_routes = get_ignore_routes(self.app)
        ignore_callbacks = get_ignore_callbacks(self.app)

        @server.before_request
        def before_request_all_events() -> None:
            if self.router.match_ignore_routes(request.path, ignore_routes):
                return None

            user_info = self._user_provider()
            event_data = self._build_event_data(user_info)

            if self.router.is_dash_callback(request.path):
                if not request.get_json():
                    return None

                body = request.get_json()
                if not body or "inputs" not in body or "output" not in body:
                    return None

                if body["output"] in ignore_callbacks:
                    return None

                if self.enable_page_view_tracking:
                    self._decide_and_track_page_view(body, ignore_routes, event_data)

                if self.enable_page_interaction_tracking:
                    self._decide_and_track_page_interaction(body, ignore_routes, event_data)

            else:
                if self.router.match_ignore_routes(request.path, ignore_routes):
                    return None

                if not self._should_track_path(request.path):
                    return None

                if self.enable_page_view_tracking:
                     self._send_event_sync("page_view", event_data)

            return None

    # #################################### #
    #     Conditional Tracking Methods     #
    # #################################### #
    def _decide_and_track_page_view(
        self, body: dict, ignore_routes: list, event_data: dict
    ) -> None:
        """
        Decide whether to track a page view event and track it.

        Args:
            body (dict): Request body
            ignore_routes (list): List of routes to ignore
            event_data (dict): Event data

        Returns:
            None
        """
        pathname = next(
            (
                inp.get("value") for inp in body["inputs"]
                if isinstance(inp, dict)
                and inp.get("property") == "pathname"
            ),
            None,
        )
        if not pathname or self.router.match_ignore_routes(pathname, ignore_routes):
            return None

        if not self._should_track_path(pathname):
            return None

        event_data["path"] = pathname
        self._send_event_sync("page_view", event_data)


    def _decide_and_track_page_interaction(
        self, body: dict,
        ignore_routes: list, event_data: dict
    ) -> None:
        """
        Decide whether to track a page interaction event and track it.
        Implements the ignore routes that are not supposed to be tracked.

        Args:
            body (dict): Request body
            ignore_routes (list): List of routes to ignore
            event_data (dict): Event data

        Returns:
            None
        """
        # TODO: Check in self.app.callback_map for page interactions
        changed_props = body.get("changedPropIds", [])
        if not changed_props:
            return None

        pathname = next(
            (
                inp.get("value") for inp in body["inputs"]
                if isinstance(inp, dict)
                and inp.get("property") == "pathname"
            ),
            None,
        )
        if pathname and self.router.match_ignore_routes(pathname, ignore_routes):
            return None

        if not self._should_track_interaction(body):
            return None

        interaction_data = event_data.copy()
        interaction_data.update(
            {
                "interaction": {
                    "changed_props": body.get("changedPropIds", []),
                    "inputs": body.get("inputs", []),
                    "outputs": body.get("outputs", []),
                    "state": body.get("state", []), # This could be a lot of data
                }
            }
        )
        self._send_event_sync("page_interaction", interaction_data)


    def _should_track_interaction(self, body: dict) -> bool:
        """
        Enhanced interaction tracking using multiple context sources
        """
        changed_props = body.get("changedPropIds", [])

        if changed_props == ['url.pathname']:
            # Ignore navigation/reload events
            return False

        if any("_pages_location.pathname" in prop for prop in changed_props):
            # This can hapen via internal dash update components and are not
            # relevant for tracking.
            return False

        return True

    def _should_track_path(self, path: str) -> bool:
        """
        Check whether the path should be tracked. This works for now
        for internal navigation tracking. It checks whether for the
        `url.pathname` or `_pages_location.pathname` change via
        `_dash-update-component` and if the path is the same as the
        referrer.

        * NOTE: Expand this method to include more complex tracking
            such as storing the last request time or method.
        """
        is_dash_update = self.router.is_dash_callback(request.path)
        is_same_path = request.referrer and path in request.referrer
        is_page_load = path == request.endpoint

        changed_props = (
            request.get_json().get("changedPropIds", [])
            if 'application/json' in request.headers.get("Content-Type", "")
            else []
        )

        # Check for page navigation in both traditional and pages plugin
        # Normally, the pages plugin uses `_pages_location.pathname` to track
        # navigation, and only `_pages_location.pathname` is updated.
        is_navigation = any(
            prop == '_pages_location.pathname' and
            '_pages_location.search' not in changed_props
            for prop in changed_props
        )

        if is_navigation:
            return True

        if is_dash_update and is_same_path:
            return False

        if is_page_load:
            return True

        return False

    # #################################### #
    #     Setup Tracking Configuration     #
    # #################################### #
    def _setup_tracking(self) -> None:
        """
        Setup tracking configuration including:
        - Server secret key
        - Repository initialization
        - Print mode configuration
        - Page view tracking
        - Page Interaction tracking
        """
        if not self.app.server.config.get("SECRET_KEY"):
            print(" * No secret key found in the server configuration. Generating a random one.")
            self.app.server.secret_key = secrets.token_hex(16)

        if self.repository:
            print(" * Using custom repository for tracking data.")
        elif self.tracker_endpoint:
            print(" * Initializing HTTP repository for tracking data.")
            self.repository = HttpTrackerRepository(self.tracker_endpoint, self.api_key)
        else:
            print(" * No tracker endpoint or repository supplied.")
            print(" * Tracking will be printed to console (development mode).")
            self._should_print = True

        if self.repository:
            from .analytics import TrackerAnalytics
            self.analytics = TrackerAnalytics(repository = self.repository)
            print(" * Analytics capabilities enabled.")

        if self.enable_page_view_tracking and self.enable_page_interaction_tracking:
            self._track_all_events()
            print(" * Tracking all combined events.")
        elif self.enable_page_view_tracking:
            self._track_page_view()
            print(" * Tracking page views.")
        elif self.enable_page_interaction_tracking:
            self._track_page_interaction()
            print(" * Tracking page interactions.")
