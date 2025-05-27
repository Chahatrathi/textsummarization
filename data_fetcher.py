import praw
import json
from bs4 import BeautifulSoup
import requests
from config import (
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,
    TOP_POST_LIMIT, COMMENT_UPVOTE_THRESHOLD
)

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def save_data_to_file(data, filename="reddit_data.json"):
    """
    Save fetched data to a local JSON file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def load_data_from_file(filename="reddit_data.json"):
    """
    Load data from a local JSON file.
    """
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

def fetch_reddit_post_data(url=None):
    """
    Fetch Reddit data from a URL or the top posts in the technology subreddit.
    """
    return fetch_post_from_url(url) if url else fetch_top_posts()

import praw
import json
from bs4 import BeautifulSoup # Keep this import, just in case, but we'll prioritize PRAW
import requests # Keep this import, just in case, but we'll prioritize PRAW
from config import (
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,
    TOP_POST_LIMIT, COMMENT_UPVOTE_THRESHOLD
)

# Initialize Reddit API (THIS SHOULD ALREADY BE IN YOUR FILE)
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# ... (keep save_data_to_file, load_data_from_file, fetch_reddit_post_data as they are) ...

# =====================================================================
# REPLACE THIS FUNCTION IN data_fetcher.py
# =====================================================================
def fetch_post_from_url(url):
    try:
        # PRAW needs a direct URL to a submission
        submission = reddit.submission(url=url)

        # Ensure comments are loaded
        submission.comments.replace_more(limit=0) # Expand all "More Comments" links

        post_data = {
            "post_title": submission.title,
            "post_body": submission.selftext, # Get the main post body
            "comments": []
        }

        # Gather comments based on upvote threshold
        for comment in submission.comments.list(): # Use .list() to iterate all loaded comments
            if comment.score >= COMMENT_UPVOTE_THRESHOLD and hasattr(comment, 'body'):
                post_data["comments"].append(comment.body)

        print(f"PRAW: Fetched single post. Title: '{post_data['post_title']}', Body length: {len(post_data['post_body'])}, Comments: {len(post_data['comments'])}")
        return post_data

    except Exception as e:
        print(f"PRAW Error fetching post from URL {url}: {e}")
        print("This could be due to invalid URL, network issues, or API limits. Returning empty data.")
        # Return a structured error response that app.py can handle
        return {"post_title": "Error: Could not fetch post", "post_body": "", "comments": []}

def fetch_top_posts():
    subreddit = reddit.subreddit("technology")
    top_posts = subreddit.top(limit=TOP_POST_LIMIT)
    data = []

    for post in top_posts:
        post_data = {
            "post_title": post.title,
            "post_body": post.selftext,
            "comments": []
        }
        post.comments.replace_more(limit=0)
        for comment in post.comments:
            if comment.score >= COMMENT_UPVOTE_THRESHOLD:
                post_data["comments"].append(comment.body)
        data.append(post_data)

    save_data_to_file(data)  # Save data locally
    return data
