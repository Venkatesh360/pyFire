from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


app = Flask(__name__)


cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from application import routes