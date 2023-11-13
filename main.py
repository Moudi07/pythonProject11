import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("New.json")

app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Create a reference to the Google post.
doc_ref = db.collection("Cats").document("AXujBsnBQI4GPjpD9A4y")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())