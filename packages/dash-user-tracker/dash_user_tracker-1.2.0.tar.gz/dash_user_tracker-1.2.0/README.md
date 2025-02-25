# Dash Tracker

Dash Tracker is a lightweight tracking library for Dash applications. It logs user interactions, page views, and navigation events, with support for sending data to a tracking endpoint or printing to console for development purposes.

## Features

* Tracks full-page loads and internal navigation events
* Built-in analytics capabilities for querying user activity and page views
* Captures user information from Flask sessions (ID, email, full name)
* Supports ignoring specific routes and callbacks
* Sends tracking data via HTTP requests or logs to the console
* Seamless integration with Dash and Flask
* Support for custom user providers and repositories

## Installation

```sh
pip install dash-user-tracker
```

## Basic Usage

The basic usage supports sending tracking data to a custom endpoint.

```python
from dash import Dash
from dash_user_tracker import Tracker

app = Dash(__name__)
tracker = Tracker(app, tracker_endpoint="https://your-tracker-endpoint.com")
```

### Development Mode

```python
tracker = Tracker(app)  # Will print events to console
```

## Custom Configuration

You can use the `HttpTrackerRepository` class to send tracking data to a custom endpoint.

```python
from dash import Dash
from dash_user_tracker import Tracker, HttpTrackerRepository

app = Dash(__name__)
repository = HttpTrackerRepository("https://your-tracker-endpoint.com", "api-key")
tracker = Tracker(
    app,
    ignore_route = ignore_route,
    ignore_callback = ignore_callback,
    user_provider = user_provider,
    repository = repository
)
```

### Ignoring Routes and Callbacks

The library allows you to customize the `ignore_route` and `ignore_callback` functions to exclude specific routes and callbacks from tracking.

```python
def ignore_route(route):
    return route in ["/health", "/metrics"]

def ignore_callback(callback):
    return callback in ["callback1", "callback2"]
```

### User Information

You can also customize the user provider to extract user information from the Flask session.

```python
def user_provider():
    return {
        "id": session.get("user_id"),
        "email": session.get("user_email"),
        "full_name": session.get("user_full_name")
    }
```

### Custom Repository

Alternatively, you can create your own custom repository by extending the `TrackerRepository` class.
To do this, look at the `HttpTrackerRepository` class for reference.

## Analytics

The library includes a built-in analytics module for querying user activity and page views.

Use it directly from the tracker instance, or, use the `TrackerAnalytics` class directly.

```python
tracker_analytics = tracker.analytics
# Or
from dash_user_tracker import TrackerAnalytics

tracker_analytics = TrackerAnalytics(
    repository = repository
)
# Get Page Views
page_views = await tracker_analytics.get_page_views()

# Get user activity
activity = await tracker_analytics.get_user_activity("user123")

# Get page activity
page_stats = await tracker_analytics.get_page_activity("/dashboard")

# Get user counts
total_users = await tracker_analytics.get_user_count()

# Get user counts by path
page_users = await tracker_analytics.get_user_count_by_path("/home")
```

## Event Data Format

The information sent to the tracking endpoint is in the following format:

```json
{
    "event": "page_view",
    "data": {
        "app_name": "My Dash App",
        "ip": "127.0.0.1",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "base_url": "http://127.0.0.1:8050/",
        "url": "http://127.0.0.1:8050/",
        "url_root": "http://127.0.0.1:8050/",
        "referrer": null,
        "path": "/",
        "full_path": "/?",
        "method": "GET",
        "user_id": "anonymous",
        "email": "anonymous",
        "full_name": "anonymous"
    },
    "timestamp": "2025-01-30T20:29:28.543062+00:00"
}
```
