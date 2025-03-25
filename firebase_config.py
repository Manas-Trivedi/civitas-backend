from dotenv import load_dotenv
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Load environment variables
load_dotenv()

# Use environment variable for Firebase credentials path
firebase_cred_path = os.getenv("FIREBASE_CREDENTIALS")
cred = credentials.Certificate(firebase_cred_path)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()