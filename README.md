# 🌟 Civitas Backend

Welcome to the **Civitas Backend**! This project powers the backend for Civitas, a platform designed to analyze and flag potentially harmful content using cutting-edge AI models like MetaHateBERT and Gemini. 🚀

## 🛠️ Features

- **Reddit Fetcher**: Fetch the latest posts from any subreddit.
- **Hate Speech Detection**: Analyze text for hate speech using MetaHateBERT.
- **Sentiment Analysis**: Use Gemini for advanced sentiment analysis.
- **Firestore Integration**: Store flagged content in a Firebase Firestore database.
- **FastAPI**: A blazing-fast API framework for seamless integration.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1️⃣ Prerequisites

Make sure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)
- **Firebase Project** with Firestore enabled
- **Hugging Face Account** (for MetaHateBERT model)

---

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/Manas-Trivedi/civitas-backend.git
cd civitas-backend
```

---

### 3️⃣ Install Dependencies

Create a virtual environment and install the required Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the root directory and add the following:

```env
REDDIT_USERNAME=your_reddit_username
REDDIT_CLIENT_SECRET=your_reddit_client_secret
GEMINI_API_KEY=your_gemini_api_key
FIREBASE_CREDS_BASE64=your_base64_encoded_firebase_credentials
```

---

### 5️⃣ Run the Application

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## 📚 API Endpoints

### 1️⃣ Analyze Text

- **Endpoint**: `/analyze`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "text": "Your text here"
  }
  ```
- **Response**:
  ```json
  {
    "post_id": "unique-id",
    "label": "LABEL_1",
    "score": 0.95,
    "action": "flagged",
    "gemini_sentiment": null,
    "gemini_score": null
  }
  ```

### 2️⃣ Fetch Reddit Posts

- **Endpoint**: `/api/fetch-reddit`
- **Method**: `GET`
- **Query Parameters**:
  - `subreddit`: Name of the subreddit (default: `confessions`)
  - `limit`: Number of posts to fetch (default: `5`)

---

## 🛡️ Security

- **Environment Variables**: Sensitive credentials are stored in the `.env` file.
- **Firestore Rules**: Ensure your Firestore database has proper security rules to prevent unauthorized access.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---