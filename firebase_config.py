import os
import base64
import json
import firebase_admin
from firebase_admin import credentials

# Decode the Base64 environment variable
firebase_creds = base64.b64decode(os.getenv("FIREBASE_CREDS_BASE64")).decode("utf-8")

# Convert string to dictionary
firebase_config = json.loads(firebase_creds)

# Initialize Firebase
cred = credentials.Certificate(firebase_config)
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()