from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from firebase_config import db  # Firestore connection
from datetime import datetime
from gemini_api import analyze_with_gemini
from reddit_fetch import router as reddit_router  # Reddit fetching router
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import uuid
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://civitas-ai.netlify.app",
        "https://civitas-backend.onrender.com",
        "http://localhost:5173",  # Added localhost for local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register the Reddit fetching router
app.include_router(reddit_router, prefix="/api")

# Pydantic model for request validation
class TextRequest(BaseModel):
    text: str

# 🔥 Load MetaHateBERT model directly from Hugging Face
model_name = "irlab-udc/MetaHateBERT"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Create pipeline
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

# Store flagged content in Firestore
def store_flagged_post(text, label, score, action, gemini_sentiment=None, gemini_score=None):
    post_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    doc_ref = db.collection("flagged_posts").document(post_id)
    doc_ref.set({
        "text": text,
        "label": label,
        "score": score,
        "action": action,
        "gemini_sentiment": gemini_sentiment,
        "gemini_score": gemini_score,
        "timestamp": timestamp
    })
    return post_id

# Route to analyze text and store flagged posts
@app.post("/analyze")
def analyze_text(request: TextRequest):
    text = request.text
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    # Step 1: MetaHateBERT detection
    result = classifier(text)

    label = result[0]['label']
    score = result[0]['score']

    # Step 2: Run Gemini if not flagged
    if label != "LABEL_1" or score < 0.8:
        gemini_sentiment = analyze_with_gemini(text)
        gemini_score = gemini_sentiment.get("score", 0)
        action = "send_to_gemini"
    else:
        gemini_sentiment = None
        gemini_score = None
        action = "flagged"

    # Store in Firestore with both MetaHateBERT and Gemini results
    post_id = store_flagged_post(
        text, label, score, action, gemini_sentiment, gemini_score
    )

    # Return response
    return {
        "post_id": post_id,
        "label": label,
        "score": score,
        "action": action,
        "gemini_sentiment": gemini_sentiment,
        "gemini_score": gemini_score
    }

# Route to retrieve flagged posts
@app.get("/flagged")
def get_flagged_posts():
    flagged_posts = []
    posts_ref = db.collection("flagged_posts").stream()

    for post in posts_ref:
        flagged_posts.append(post.to_dict())

    return flagged_posts

@app.api_route("/ping", methods=["GET", "HEAD"])
def ping():
    return JSONResponse(content={"message": "Server is running"}, status_code=200)