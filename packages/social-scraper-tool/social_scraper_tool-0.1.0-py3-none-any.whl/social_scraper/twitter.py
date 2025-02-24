"""
"""
import os
from datetime import date, timedelta, datetime
from typing import List

import pandas as pd
from twscrape import API, gather, Tweet

from .models import TRPost, TRUser, TRClassification
from logging_config import logger


class TwitterScraper:
    def __init__(self):
        """
        Initializes the TwitterScraper and logs in automatically.
        """
        self.api = API()
        self._login()

    def _login(self):
        """
        Authenticates with Twitter using multiple accounts.
        """
        logger.info("Logging into Twitter...")

        for i in range(1, 10):
            if os.getenv(f"USERNAME_{i}"):
                self.api.pool.add_account(
                    os.getenv(f"USERNAME_{i}"),
                    os.getenv(f"PASSWORD_{i}"),
                    os.getenv(f"USER_EMAIL_{i}"),
                    os.getenv(f"PASSWORD_{i}")
                )

        self.api.pool.login_all()
        logger.info("Successfully logged into Twitter.")

    async def scrape(self, query: str, time_filter: str = "day", lang: str = "en", limit: int = 10) -> pd.DataFrame:
        """
        Scrapes tweets containing a specific word within a specified time range.

        :param query: The keyword or phrase to search for.
        :param time_filter: Time range for the search ("day", "yesterday", "week").
        :param lang: Language filter for the tweets (default is "en" - you can also use "pt-pt").
        :param limit: Maximum number of tweets to retrieve (default is 10).
        :return: DataFrame of processed tweets.
        """
        logger.info(f"Starting Twitter scrape for query: '{query}', time_filter: '{time_filter}', limit: {limit}.")

        now = datetime.now()
        if time_filter == "day":
            since = now.strftime('%Y-%m-%d')
            until = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        elif time_filter == "yesterday":
            since = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
            until = now.strftime('%Y-%m-%d')
        elif time_filter == "week":
            since = (date.today() - timedelta(days=6)).strftime('%Y-%m-%d')
            until = now.strftime('%Y-%m-%d')
        else:
            raise ValueError("Invalid time_filter. Use 'day', 'yesterday', or 'week'.")

        search_query = f"{query} since:{since} until:{until} lang:{lang}"
        tweets = await gather(self.api.search(search_query, limit=limit))

        logger.info(f"Fetched {len(tweets)} tweets for query: '{query}'.")
        processed_tweets = self.map_scraped_posts(tweets, query)

        df_twitter = self.posts_to_dataframe(processed_tweets)
        return df_twitter

    def map_scraped_posts(self, tweets: List[Tweet], keyword: str) -> List[TRPost]:
        """
        Maps raw Twitter data into structured TRPost objects.

        :param tweets: List of tweets.
        :param keyword: Search keyword used in the query.
        :return: List of structured TRPost objects.
        """
        logger.info("Mapping scraped tweets to structured objects...")
        mapped_posts = []

        for tweet in tweets:
            mapped_posts.append(
                TRPost(
                    id=tweet.id,
                    content=tweet.rawContent,
                    date=tweet.date,
                    engine="twitter",
                    user=TRUser(
                        username=tweet.user.username,
                        id=tweet.user.id,
                        followers=tweet.user.followersCount,
                        statuses=tweet.user.statusesCount,
                        url=tweet.user.url,
                        verified=tweet.user.verified
                    ),
                    classification=TRClassification(
                        label=keyword,
                        likes=tweet.likeCount,
                        views=tweet.viewCount,
                        replies=tweet.replyCount
                    ),
                    url=tweet.url
                )
            )

        logger.info("Successfully mapped tweets.")
        return mapped_posts

    def posts_to_dataframe(self, posts: List[TRPost]) -> pd.DataFrame:
        """
        Converts structured TRPost objects into a Pandas DataFrame.

        :param posts: List of TRPost objects.
        :return: DataFrame representation of posts.
        """
        return pd.DataFrame([post.__dict__ for post in posts])
