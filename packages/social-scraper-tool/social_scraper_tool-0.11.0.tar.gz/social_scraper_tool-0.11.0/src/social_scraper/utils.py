"""
"""
import pandas as pd
from typing import List

from .models import TRPost


# Assume TRClassification, TRUser, and TRPost are defined as above.
def posts_to_dataframe(posts: List[TRPost], csv: bool = False, file_path: str = "posts.csv") -> pd.DataFrame:
    """
    Converts a list of TRPost objects into a Pandas DataFrame.

    Args:
        posts (List[TRPost]): A list of TRPost objects.
        csv (bool, optional): If True, convert to Pandas DataFrame. Defaults to False.
        file_path (str, optional): If provided, convert to Pandas DataFrame. Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing the structured data from the posts.
    """
    # Extract data from each TRPost object
    data = []
    for post in posts:
        data.append({
            "post_id": post.id,
            "content": post.content,
            "url": post.url,
            "date": post.date,
            "platform": post.platform,
            "username": post.user.username,
            "user_id": post.user.id,
            "followers": post.user.followers,
            "statuses": post.user.statuses,
            "user_url": post.user.url,
            "verified": post.user.verified,
            "label": post.classification.label,
            "likes": post.classification.likes,
            "views": post.classification.views,
            "replies": post.classification.replies,
        })

    # Convert to DataFrame
    posts = pd.DataFrame(data)
    if csv:
        posts.to_csv(file_path, index=False)

    return posts
