from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

class TrackerRepository(ABC):
    """Abstract class for tracker data access"""

    @abstractmethod
    async def get_page_views(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> dict:
        pass

    @abstractmethod
    async def get_page_views_by_user(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> dict:
        pass

    @abstractmethod
    async def get_page_views_by_path(
        self,
        path: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
        limit: Optional[int] = None,
    ) -> dict:
        pass

    @abstractmethod
    async def get_user_count(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        pass

    @abstractmethod
    async def get_user_count_by_path(
        self,
        path: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        pass

    @abstractmethod
    async def get_page_count(
        self,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        pass

    @abstractmethod
    async def get_page_count_by_user(
        self,
        user_id: str,
        start: Optional[datetime] = None,
        end: Optional[datetime] = None,
    ) -> int:
        pass

    @abstractmethod
    async def save_event(
        self,
        event: dict,
    ) -> None:
        pass
