import firebase_admin
from firebase_admin import credentials, auth, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        return user.uid
    except:
        return None

def login_user(email):
    try:
        user = auth.get_user_by_email(email)
        return user.uid
    except:
        return None
