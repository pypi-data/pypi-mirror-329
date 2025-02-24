from reddit import RedditScraper
from dotenv import load_dotenv

from utils import posts_to_dataframe

load_dotenv()

reddit_scraper = RedditScraper()
reddit_posts = reddit_scraper.get_posts(query="AI", subreddit="technology", time_filter="week", limit=1)

df_reddit_posts = posts_to_dataframe(reddit_posts)

print(df_reddit_posts.head())

from twitter import TwitterScraper
import asyncio

async def fetch_twitter_posts():
    twitter_scraper = TwitterScraper()
    await twitter_scraper.login()
    posts = await twitter_scraper.get_posts(query="AI technology", limit=1)
    return posts
twitter_posts = asyncio.run(fetch_twitter_posts())

df_twitter_posts = posts_to_dataframe(twitter_posts)
print(df_twitter_posts.head())
