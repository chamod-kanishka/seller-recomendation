# -----Imports-----
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from json import JSONEncoder

from UsingAlgorithm import get_recommendation, update_recommendation_system
from TrainingAlgorithm import train_recommendation_system

# -----App initalization-----
app = Flask(__name__)
CORS(app)

# -----API endpoints-----
# Train
@app.route('/train', methods=['GET'])
def train():
    # Train
    train = train_recommendation_system()

    if train:
        return jsonify({"result": "Successfully trained!"}), 200
    else:
        return jsonify({"error": "Failed to train"}), 400

# Get recommendation
@app.route('/recommend', methods=['GET'])
def recommend():
    # Validate req params
    if "userid" not in request.args:
        return jsonify({"error": "User id not provided!"}), 400
    
    if "usercount" not in request.args:
        return jsonify({"error": "User count not provided!"}), 400

    if "sellercount" not in request.args:
        return jsonify({"error": "Seller count not provided!"}), 400
    
    # Get params
    user_id = request.args.get('userid')
    user_count = request.args.get('usercount')
    seller_count = request.args.get('sellercount')

    # Validate user id
    if user_id == "":
        return jsonify({"error": "User id is empty!"}), 400
    
    # Validate user count
    if user_count == 0 or user_count == "":
        return jsonify({"error": "User count is 0 or empty!"}), 400
    
    # Validate seller count
    if seller_count == 0 or seller_count == "":
        return jsonify({"error": "Seller count is 0 or empty!"}), 400

    try:
        # Get the prediction
        seller_id = get_recommendation(user_count, seller_count, user_id)

        return jsonify({"result": seller_id}), 200
    except Exception as e:
        return jsonify({"error": "Failed to get the recommended seller!"}), 400
        
# Update recommendation system
@app.route('/update', methods=['GET'])
def update():
    # Validate req params
    if "userid" not in request.args:
        return jsonify({"error": "User id not provided!"}), 400
    
    if "usercount" not in request.args:
        return jsonify({"error": "User count not provided!"}), 400

    if "sellercount" not in request.args:
        return jsonify({"error": "Seller count not provided!"}), 400

    if "recommendedseller" not in request.args:
        return jsonify({"error": "Recommended seller not provided!"}), 400

    if "reward_product" not in request.args:
        return jsonify({"error": "Reward product not provided!"}), 400
    
    if "reward_delivery" not in request.args:
        return jsonify({"error": "Reward delivery not provided!"}), 400
    
    if "reward_communication" not in request.args:
        return jsonify({"error": "Reward communication not provided!"}), 400
    
    # Get params
    user_id = request.args.get('userid')
    user_count = request.args.get('usercount')
    seller_count = request.args.get('sellercount')
    recommended_seller = request.args.get('recommendedseller')
    reward_product = request.args.get('reward_product')
    reward_delivery = request.args.get('reward_delivery')
    reward_communication = request.args.get('reward_communication')

    # Validate user id
    if user_id == "":
        return jsonify({"error": "User id is empty!"}), 400
    
    # Validate user count
    if user_count == 0 or user_count == "":
        return jsonify({"error": "User count is 0 or empty!"}), 400
    
    # Validate seller count
    if seller_count == 0 or seller_count == "":
        return jsonify({"error": "Seller count is 0 or empty!"}), 400

    # Validate recommended seller
    if recommended_seller == "":
        return jsonify({"error": "Recommended seller is empty!"}), 400

    # Validate reward
    if reward_product is None or reward_product == "" or (isinstance(reward_product, (int, float)) and (reward_product < -1.0 or reward_product > 1.0)):
        return jsonify({"error": "Reward product is lesser or greater than expected or empty!"}), 400
    
    if reward_delivery is None or reward_delivery == "" or (isinstance(reward_delivery, (int, float)) and (reward_delivery < -1.0 or reward_delivery > 1.0)):
        return jsonify({"error": "Reward delivery is lesser or greater than expected or empty!"}), 400
    
    if reward_communication is None or reward_communication == "" or (isinstance(reward_communication, (int, float)) and (reward_communication < -1.0 or reward_communication > 1.0)):
        return jsonify({"error": "Reward communication is lesser or greater than expected or empty!"}), 400

    # Update
    update = update_recommendation_system(user_count, seller_count, user_id, recommended_seller, reward_product, reward_delivery, reward_communication)

    if update:
        return jsonify({"result": "Successfully updated!"}), 200
    else:
        return jsonify({"error": "Failed to update"}), 400

# -----Execute the app-----
if __name__ == "__main__":
    app.run(host="0.0.0.0")
