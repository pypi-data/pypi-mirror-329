from reddit import RedditScraper
from dotenv import load_dotenv

load_dotenv()

reddit_scraper = RedditScraper()
df_reddit = reddit_scraper.get_posts(query="AI", subreddit="technology", time_filter="week", limit=10)

print(df_reddit.head())