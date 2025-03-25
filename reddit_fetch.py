import requests
from fastapi import APIRouter, HTTPException

# Create a FastAPI router for Reddit fetching
router = APIRouter()

# Route to fetch Reddit posts
@router.get("/fetch-reddit")
def fetch_reddit(subreddit: str = "confessions", limit: int = 5):
    try:
        url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
        headers = {"User-Agent": "Civitas/0.1"}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch Reddit posts")

        reddit_data = response.json()

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

        return {"subreddit": subreddit, "posts": posts}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Reddit posts: {str(e)}")