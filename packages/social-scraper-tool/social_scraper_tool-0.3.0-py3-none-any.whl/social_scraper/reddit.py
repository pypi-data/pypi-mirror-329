"""
"""
import os
from datetime import datetime
from typing import List

import praw

from .models import TRPost, TRUser, TRClassification
from .logging_config import logger


class RedditScraper:
    def __init__(self):
        try:
            self.reddit = praw.Reddit(
                username=os.getenv("USERNAME_REDDIT"),
                password=os.getenv("PASSWORD_REDDIT"),
                client_id=os.getenv("CLIENT__ID_REDDIT"),
                client_secret=os.getenv("CLIENT_SECRET"),
                user_agent=os.getenv("USER_AGENT_REDDIT")
            )
            logger.info("RedditScraper initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize RedditScraper: {e}")
            raise

    def get_posts(self, query: str = None, subreddit: str = "all", time_filter: str = "week", limit=10):
        logger.info(f"Starting Reddit scrape for query: '{query}'; subreddit: '{subreddit}';"
                    f" time_filter: '{time_filter}'; limit: {limit}.")

        if query:
            logger.info(f"Searching for '{query}' in r/{subreddit}, time_filter: '{time_filter}', limit: {limit}.")
        else:
            logger.info(f"Fetching top posts from r/{subreddit}, time_filter: '{time_filter}', limit: {limit}.")

        try:
            reddit_posts = []

            if query:
                # Search for a keyword in the subreddit
                for submission in self.reddit.subreddit("all").search(query, time_filter=time_filter, limit=limit):
                    reddit_posts.append(submission)
            else:
                # Get top posts from the subreddit if no keyword is provided
                for submission in self.reddit.subreddit(subreddit).top(time_filter=time_filter, limit=limit):
                    reddit_posts.append(submission)

            logger.info(f"Successfully fetched {len(reddit_posts)} posts from r/{subreddit}.")

            # Map and process the scraped posts
            mapped_posts = self.map_scraped_posts(reddit_posts, query if query else subreddit)
            # df_reddit = self.posts_to_dataframe(mapped_posts)

            logger.info("Successfully mapped posts to DataFrame.")
            return mapped_posts
        except Exception as e:
            logger.error(f"Error during scraping process in r/{subreddit}. Error: {e}")
            raise

    def map_scraped_posts(self, reddit_posts: List, word: str) -> list:
        """
        Maps raw Reddit posts to a list of TRPost objects.

        :param reddit_posts: List of Reddit post submissions.
        :param word: The search keyword for classification.
        :return: List of TRPost objects.
        """
        logger.info("Mapping scraped Reddit posts...")

        list_of_scraped_posts = []

        try:
            for reddit_post in reddit_posts:
                try:
                    # Process top-level comments for each post
                    for top_level_comment in reddit_post.comments:
                        if isinstance(top_level_comment, praw.models.Comment):
                            author = top_level_comment.author

                            list_of_scraped_posts.append(
                                TRPost(
                                    id=top_level_comment.subreddit_id,
                                    content=top_level_comment.body if top_level_comment.body else "DELETED",
                                    date=datetime.fromtimestamp(top_level_comment.created_utc),
                                    engine="reddit",
                                    user=TRUser(
                                        username=author.name if author else "UNKNOWN",
                                        id=author.id if author else "UNKNOWN",
                                        statuses=author.total_karma if author else 0,
                                        verified=author.has_verified_email if author else False
                                    ),
                                    classification=TRClassification(
                                        word,
                                        top_level_comment.score
                                    )
                                )
                            )
                except Exception as comment_error:
                    logger.warning(f"Error processing comments for post ID {reddit_post.id}. Error: {comment_error}")

                try:
                    # Process the main post itself
                    author = reddit_post.author

                    list_of_scraped_posts.append(
                        TRPost(
                            id=reddit_post.id,
                            content=reddit_post.selftext if reddit_post.selftext else reddit_post.title,
                            date=datetime.fromtimestamp(reddit_post.created_utc),
                            engine="reddit",
                            user=TRUser(
                                username=author.name if author else "UNKNOWN",
                                id=author.id if author else "UNKNOWN",
                                statuses=author.total_karma if author else 0,
                                verified=author.has_verified_email if author else False
                            ),
                            classification=TRClassification(
                                word,
                                reddit_post.score,
                                reddit_post.view_count,
                                reddit_post.num_comments
                            ),
                            url=reddit_post.url
                        )
                    )
                except Exception as post_error:
                    logger.warning(f"Error processing post ID {reddit_post.id}. Error: {post_error}")

            logger.info("Successfully mapped all Reddit posts.")
            return list_of_scraped_posts

        except Exception as e:
            logger.error(f"Failed to map Reddit posts. Error: {e}")
            raise

