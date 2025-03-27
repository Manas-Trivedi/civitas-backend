from google import genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Gemini Sentiment Analysis Function
def analyze_with_gemini(text):
    try:
        response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=f"""
        Analyze the following text for **any form of harmful, offensive, or inappropriate content**,
        making it suitable for all audiences, including children.

        Consider the following:
        - **Hate speech:** slurs, derogatory language, or harmful stereotypes.
        - **Insults or rudeness:** personal attacks, name-calling, or condescending remarks.
        - **Explicit content:** violent, sexual, or otherwise inappropriate material.
        - **Negative sentiment:** overly aggressive or mean-spirited language.

        Provide the result in JSON format with two fields:
        - "score" (0-100) indicating how inappropriate the content is.
        - "sentiment" (1-5 words describing the sentiment).

        Text: {text}
        """
    )

        # Extract the response text
        response_text = response.candidates[0].content.parts[0].text.strip()

        # ✅ Strip backticks if present
        if response_text.startswith("```json") and response_text.endswith("```"):
            response_text = response_text[7:-3].strip()

        # Ensure valid JSON format
        try:
            sentiment_data = json.loads(response_text)
        except json.JSONDecodeError:
            print("Failed to parse JSON response from Gemini:", response_text)
            return {"score": None, "sentiment": "Parsing error"}

        return sentiment_data

    except Exception as e:
        print("Gemini API error:", e)
        return {"score": None, "sentiment": "API error"}