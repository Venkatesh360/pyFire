from firebase_admin import firestore
from flask import jsonify, request
from application import app, db
from functions.recommender import get_recommendations, get_data
from dotenv import load_dotenv
import os

load_dotenv()
accessKey = os.getenv("FRONTEND_KEY")

@app.route("/")
def index():
    return "<h1> hello </h1>"

@app.route("/create_user", methods=["POST"])
def create_user():
    try:
        data = request.json
        uid = data.get("userId")
        key = data.get("key")
        
        accessKey = os.getenv("FRONTEND_KEY")
        
        if not accessKey == key:
            return jsonify({
	            "message": "Invalid API key: You must be granted a valid key.",
            }), 401
        
        collection_ref = db.collection("users")
        doc_ref = collection_ref.document(str(uid))
        recommendations = get_data(get_recommendations([19995, 27205, 157336, 293660, 550]))
        movie_data = {
            "watched": [],
            "watchlist": [],
            "recommendations": recommendations
        }
        
        doc_ref.set(movie_data)
        
        return jsonify({
            "message": "Document created successfully",
            "uid": uid,
            "data": movie_data
        }), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/add_to_recommendation", methods=["PUT"])
def add_recommendation():
    data = request.json
    uid = data.get("uid")
    movieId = data.get("movieId")
    key = data.get("key")
    
    if not accessKey == key:
        
        return jsonify({
	            "message": "Invalid API key: You must be granted a valid key.",
        }), 401
      
    if uid is None or movieId is None:
        return jsonify({'error': 'uid and movieId are required'}), 400
    
    doc_ref = db.collection("users").document(uid)
    doc = doc_ref.get()
    
    if not doc.exists:
        return jsonify({"error": "User not found"}), 404
    
    user_data = doc.to_dict()
    recommendations = user_data.get("recommendations", [])
    watched = user_data.get("watched", [])
    watched.append(int(movieId))
    
    similar = get_data(get_recommendations([movieId]))
    
    recommendations.extend(similar)
    
    # Remove watched items from recommendations
    recommendations = [rec for rec in recommendations if rec['id'] not in watched]

    doc_ref.update({
        "recommendations": recommendations,
        "watched": watched
    })
    
    return jsonify({"message": "Recommendations updated successfully"}), 200

@app.route("/remove_from_recommendation", methods=["PUT"])
def remove_recommendations():
    data = request.json
    uid = data.get("uid")
    movieId = data.get("movieId")
    key = data.get("key")
    
    if not accessKey == key:
        
        return jsonify({
	            "message": "Invalid API key: You must be granted a valid key.",
        }), 401
     
    if uid is None or movieId is None:
        return jsonify({'error': 'uid and movieId are required'}), 400
    
    doc_ref = db.collection("users").document(uid)
    doc = doc_ref.get()
    
    if not doc.exists:
        return jsonify({"error": "User not found"}), 404
    
    user_data = doc.to_dict()
    recommendations = user_data.get("recommendations", [])
    watched = user_data.get("watched", [])
    watched.append(int(movieId))
    
    similar = get_recommendations([movieId])
    
    # Remove similar items from recommendations
    recommendations = [rec for rec in recommendations if rec['id'] not in similar]

    doc_ref.update({
        "recommendations": recommendations,
        "watched": watched
    })
    
    return jsonify({"message": "Recommendations updated successfully"}), 200