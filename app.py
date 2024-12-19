from flask import Flask, jsonify, request
from leaderboard import LeaderBoard
import json

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    leaderboard = LeaderBoard()
    competition_name = request.args['competition_name']
    return jsonify(leaderboard.get_kaggle_leaderboard(competition_name=competition_name))


if __name__ == '__main__':
    app.run(debug=True)