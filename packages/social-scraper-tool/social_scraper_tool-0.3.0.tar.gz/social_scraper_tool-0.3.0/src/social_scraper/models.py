"""
Module for data representation of TR posts, users, and classifications. This module defines data classes for handling
structured data such as classifications, users, and posts with their respective attributes.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union


@dataclass
class TRClassification:
    """
    Represents a classification result for a post.

    Attributes:
        label (str): The label assigned by the classification model (e.g., 'positive', 'negative').
        likes (Optional[float]): The number of likes the post received.
        views (Optional[float]): The number of views the post received.
        replies (Optional[float]): The number of replies the post received.
    """
    label: str
    likes: Optional[float] = 0
    views: Optional[float] = 0
    replies: Optional[float] = 0


@dataclass
class TRUser:
    """
    Represents a user in the system.

    Attributes:
        id (Optional[int]): The unique identifier of the user.
        username (str): The username of the user.
        followers (Optional[Union[int, str]]): The number of followers the user has.
        statuses (Optional[Union[int, str]]): The user's current status count or bio.
        url (Optional[str]): The URL to the user's profile.
        verified (Optional[bool]): Whether the user's account is verified.
    """
    username: Optional[str] = "UNKNOWN"
    id: Optional[Union[int, str]] = 0
    followers: Optional[Union[int, str]] = 0
    statuses: Optional[Union[int, str]] = 0
    url: Optional[str] = "UNKNOWN"
    verified: Optional[bool] = False


@dataclass
class TRPost:
    """
    Represents a post in the system.

    Attributes:
        id (Union[str, int]): The unique identifier of the post.
        content (str): The content of the post.
        url (str): The URL to the post.
        date (datetime): The date and time when the post was created.
        engine (str): The engine of the post (twitter, reddit, etc.).
        user (TRUser): The user who created the post.
        classification (TRClassification): The classification result associated with the post.
    """
    id: Union[str, int]
    content: str
    date: datetime
    engine: str
    user: TRUser
    classification: TRClassification
    url: Optional[str] = "UNKNOWN"
