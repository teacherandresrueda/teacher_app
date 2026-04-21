import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json

if not firebase_admin._apps:

    firebase_dict = json.loads(st.secrets["firebase_json"])

    firebase_dict["private_key"] = firebase_dict["private_key"].replace("\\n", "\n")

    cred = credentials.Certificate(firebase_dict)

    firebase_admin.initialize_app(cred)

db = firestore.client()
