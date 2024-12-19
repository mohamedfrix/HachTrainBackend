from flask import Flask, jsonify, request
from flask_cors import CORS
from leaderboard import LeaderBoard
import json

app = Flask(__name__)

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    leaderboard = LeaderBoard()
    competition_name = request.args.get('competition_name')  # Safer to use .get() instead of indexing directly
    data = leaderboard.get_kaggle_leaderboard(competition_name=competition_name)
    return jsonify(data)

@app.route('/')
def home():
    return "Hello, Flask!"



if __name__ == '__main__':
    app.run(debug=True)