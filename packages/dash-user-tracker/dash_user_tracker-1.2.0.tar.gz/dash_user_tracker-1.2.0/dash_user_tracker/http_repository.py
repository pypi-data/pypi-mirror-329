from .repository import TrackerRepository
import aiohttp
from typing import List, Optional
from datetime import datetime

class HttpTrackerRepository(TrackerRepository):
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

    async def get_page_views(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """
        Get page views from the tracker API

        Args:
            start (datetime): Start date for the query
            end (datetime): End date for the query
            limit (int): Maximum number of results to return

        Returns:
            List of page views
        """
        async with aiohttp.ClientSession() as session:
            params = {}
            if start:
                params['start'] = start.isoformat()
            if end:
                params['end'] = end.isoformat()
            if limit:
                params['limit'] = limit

            headers = {'X-API-Key': self.api_key}

            async with session.get(
                f"{self.endpoint}/page-views", params = params,
                headers = headers,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def get_page_views_by_user(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """
        Get page views from the tracker API for a specific user

        Args:
            user_id (str): User ID to filter by
            start (datetime): Start date for the query
            end (datetime): End date for the query
            limit (int): Maximum number of results to return

        Returns:
            List of page views
        """
        async with aiohttp.ClientSession() as session:
            params = {}
            if start:
                params['start'] = start.isoformat()
            if end:
                params['end'] = end.isoformat()
            if limit:
                params['limit'] = limit

            headers = {'X-API-Key': self.api_key}

            async with session.get(
                f"{self.endpoint}/page-views/user/{user_id}", params = params,
                headers = headers,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def get_page_views_by_path(
        self,
        path: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> dict:
        """
        Get page views from the tracker API for a specific path

        Args:
            path (str): Path to filter by
            start (datetime): Start date for the query
            end (datetime): End date for the query
            limit (int): Maximum number of results to return

        Returns:
            List of page views
        """
        async with aiohttp.ClientSession() as session:
            params = {'path': path}
            if start:
                params['start'] = start.isoformat()
            if end:
                params['end'] = end.isoformat()
            if limit:
                params['limit'] = limit

            headers = {'X-API-Key': self.api_key}

            async with session.get(
                f"{self.endpoint}/page-views/path", params = params,
                headers = headers,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def get_user_count(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        """
        Get the number of unique users from the tracker API

        Args:
            start (datetime): Start date for the query
            end (datetime): End date for the query

        Returns:
            Number of unique users
        """
        async with aiohttp.ClientSession() as session:
            params = {}
            if start:
                params['start'] = start.isoformat()
            if end:
                params['end'] = end.isoformat()

            headers = {'X-API-Key': self.api_key}

            async with session.get(
                f"{self.endpoint}/page-views/user-count", params = params,
                headers = headers,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def get_user_count_by_path(
        self,
        path: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        """
        Get the number of unique users from the tracker API

        Args:
            path (str): Path to filter by
            start (datetime): Start date for the query
            end (datetime): End date for the query

        Returns:
            Number of unique users
        """
        if not path:
            raise ValueError("Path is required")

        async with aiohttp.ClientSession() as session:
            params = {'path': path}
            if start:
                params['start'] = start.isoformat()
            if end:
                params['end'] = end.isoformat()

            headers = {'X-API-Key': self.api_key}

            async with session.get(
                f"{self.endpoint}/page-views/user-count", params = params,
                headers = headers,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def get_page_count(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        """
        Get the number of page views from the tracker API

        Args:
            start (datetime): Start date for the query
            end (datetime): End date for the query

        Returns:
            Number of page views
        """
        async with aiohttp.ClientSession() as session:
            params = {}
            if start:
                params['start'] = start.isoformat()
            if end:
                params['end'] = end.isoformat()

            headers = {'X-API-Key': self.api_key}

            async with session.get(
                f"{self.endpoint}/page-views/page-count", params = params,
                headers = headers,
            ) as response:
                response.raise_for_status()
                return await response.json()

    async def get_page_count_by_user(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        """
        Get the number of page views from the tracker API

        Args:
            user_id (str): User ID to filter by
            start (datetime): Start date for the query
            end (datetime): End date for the query

        Returns:
            Number of page views
        """
        if not user_id:
            raise ValueError("User ID is required")

        async with aiohttp.ClientSession() as session:
            params = {'user_id': user_id}
            if start:
                params['start'] = start.isoformat()
            if end:
                params['end'] = end.isoformat()

            headers = {'X-API-Key': self.api_key}

            async with session.get(
                f"{self.endpoint}/page-views/page-count", params = params,
                headers = headers,
            ) as response:
                response.raise_for_status()
                return await response.json()


    async def save_event(
        self,
        event: dict,
    ) -> None:
        """
        Save an event to the tracker API

        Args:
            event (dict): Event data
        """
        async with aiohttp.ClientSession() as session:
            headers = {'X-API-Key': self.api_key}

            async with session.post(
                f"{self.endpoint}", json = event,
                headers = headers,
            ) as response:
                response.raise_for_status()
