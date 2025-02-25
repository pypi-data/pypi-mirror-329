from datetime import datetime
from typing import List, Optional

from .http_repository import HttpTrackerRepository
from .repository import TrackerRepository


class TrackerAnalytics:
    """Class for querying and analyzing tracker data."""

    def __init__(
        self,
        tracker_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        repository: Optional[TrackerRepository] = None,
    ):
        """
        Initialize the tracker analytics.

        Args:
            tracker_endpoint (Optional[str], optional): string endpoint
                for tracking, if not supplied, actions will be printed
                to console. Defaults to None.
            api_key (Optional[str], optional): API key for tracking server.
                Defaults to None.
            repository (Optional[TrackerRepository], optional): A repository
                for tracking navigation data. Defaults to None.
        """
        self.repository = repository
        if not repository and tracker_endpoint:
            self.repository = HttpTrackerRepository(tracker_endpoint, api_key)
        elif not repository and not tracker_endpoint:
            raise ValueError("No repository or tracker endpoint supplied.")

    async def get_page_views(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """Get page views from the tracker within the specified time range."""
        return await self.repository.get_page_views(start, end, limit)

    async def get_user_activity(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> dict:
        """Get activity data for the specific user. Returns
        a dictionary with the total views, unique pages, and page views, in the
        current format:
        ```json
        {
            "total_views": 0,
            "unique_pages": {
                "count": 0,
                "pages": []
            },
            "page_views": []
        }
        ```
        """
        page_views = await self.repository.get_page_views_by_user(user_id, start, end)
        unique_pages = set(pv['path'] for pv in page_views.get('data', []))
        return {
            "total_views": page_views.get("count", 0),
            "unique_pages": {
                "count": len(unique_pages),
                "pages": list(unique_pages),
            },
            "page_views": page_views.get("data", []),
        }

    async def get_page_activity(
        self,
        path: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> dict:
        """Get activity data for the specific page. Returns
        a dictionary with the total views, unique users, and page views, in the
        current format:
        ```json
        {
            "total_views": 0,
            "unique_users": {
                "count": 0,
                "user_ids": []
                "user_emails": []
            },
            "page_views": []
        }
        ```
        """
        page_views = await self.repository.get_page_views_by_path(path, start, end)
        unique_users_id = set(pv['user_id'] for pv in page_views.get('data', []))
        unique_users_email = set(pv['email'] for pv in page_views.get('data', []))

        return {
            "total_views": page_views.get("count", 0),
            "unique_users": {
                "count": len(unique_users_id),
                "user_ids": list(unique_users_id),
                "user_emails": list(unique_users_email),
            },
            "page_views": page_views.get("data", []),
        }

    async def get_user_count(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        """Get the number of unique users within the specified time range."""
        return await self.repository.get_user_count(start, end)

    async def get_user_count_by_path(
        self,
        path: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        """Get the number of unique users that visited a specific page within the specified time range."""
        return await self.repository.get_user_count_by_path(path, start, end)

    async def get_page_count(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        """Get the number of pages within the specified time range."""
        return await self.repository.get_page_count(start, end)

    async def get_page_count_by_user(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        """Get the number of pages that were visited by a user within the specified time range."""
        return await self.repository.get_page_count_by_user(user_id, start, end)
