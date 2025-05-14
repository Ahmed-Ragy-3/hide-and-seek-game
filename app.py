from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from game import Game
import util as u

app = Flask(__name__)
CORS(app)

game: Game = None
current_player: u.PLAYER = None


@app.route('/game', methods=['POST'])
def create_game():
   global game, current_player
   data = request.get_json()
   N = data.get('N')
   M = data.get('M', 1)
   role = data.get('role', 'hider').lower()

   if N is None or role not in ('hider', 'seeker'):
      return jsonify({'error': 'Invalid input'}), 400

   current_player = u.PLAYER.HIDER if role == 'hider' else u.PLAYER.SEEKER
   game = Game(N=N, M=M)

   return jsonify({
      'message': f'Game created with {N} columns and role: {role}',
      'world': [[cell.value for cell in row] for row in game.world]
   })


@app.route('/round', methods=['POST'])
def play_round():
   if not game:
      return jsonify({'error': 'Game not initialized'}), 400

   human_move = request.get_json().get('move')  # (row, col)

   # Let the computer play optimally
   computer_move = game.play_round(game.other(current_player))

   return jsonify({
      'human_move': human_move,
      'computer_move': computer_move,
      'current_player': current_player.name
   })


@app.route('/simulate', methods=['POST'])
def simulate_game():
   from play import simulate  # Import your simulate logic
   results = simulate(game, rounds=100, start_turn=current_player)

   return jsonify({
      'rounds': len(results),
      'results': results
   })


@app.route('/state', methods=['GET'])
def get_game_state():
   if not game:
      return jsonify({'error': 'Game not initialized'}), 400

   return jsonify({
      'payoff_matrix': game.get_payoff_matrix().tolist(),
      'hider_probabilities': game.hider_probabilities.tolist() if game.hider_probabilities is not None else [],
      'seeker_probabilities': game.seeker_probabilities.tolist() if game.seeker_probabilities is not None else [],
      'world': [[cell.value for cell in row] for row in game.world]
   })


@app.route('/reset', methods=['POST'])
def reset_game():
   if not game:
      return jsonify({'error': 'Game not initialized'}), 400
   game.reset()
   return jsonify({'message': 'Game reset'})


if __name__ == '__main__':
   app.run(debug=True)
