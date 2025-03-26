import requests
from fastapi import APIRouter, HTTPException
import logging
import traceback
from dotenv import load_dotenv
import os

# Configure logging
logging.basicConfig(level=logging.INFO)  # Change to DEBUG for more verbosity

load_dotenv()
router = APIRouter()

@router.get("/fetch-reddit")
def fetch_reddit(subreddit: str = "confessions", limit: int = 5):
    try:
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        auth = (os.getenv("REDDIT_USERNAME"), os.getenv("REDDIT_CLIENT_SECRET"))

        # Log the request details
        logging.info(f"Fetching Reddit posts from URL: {url} with headers: {headers}")

        response = requests.get(url, headers=headers, auth=auth)

        # Log the response details
        logging.info(f"Reddit API Response: {response.status_code}")
        logging.debug(f"Response Body: {response.text}")

        if response.status_code != 200:
            logging.error(f"Failed to fetch Reddit posts. Status: {response.status_code}, Body: {response.text}")
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch Reddit posts")

        reddit_data = response.json()

        # Validate the response structure
        if "data" not in reddit_data or "children" not in reddit_data["data"]:
            logging.error(f"Unexpected Reddit API response format: {reddit_data}")
            raise HTTPException(status_code=500, detail="Unexpected Reddit API response format")

        # Extract relevant post data
        posts = []
        for post in reddit_data['data']['children']:
            data = post['data']
            posts.append({
                "title": data.get("title", "No title"),
                "text": data.get("selftext", ""),
                "author": data.get("author", "Unknown"),
                "subreddit": data.get("subreddit", "N/A"),
                "upvotes": data.get("ups", 0),
                "downvotes": data.get("downs", 0),
                "url": f"https://www.reddit.com{data.get('permalink', '')}",
                "created_utc": data.get("created_utc", "")
            })

        logging.info(f"Successfully fetched {len(posts)} posts from subreddit: {subreddit}")
        return {"subreddit": subreddit, "posts": posts}

    except Exception as e:
        # Log the full traceback for debugging
        logging.error(f"Error fetching Reddit posts: {str(e)}")
        logging.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error fetching Reddit posts: {str(e)}")