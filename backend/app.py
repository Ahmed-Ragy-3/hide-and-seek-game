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
    game = None
    current_player = None
    data = request.get_json()
    N = data.get('N')
    M = data.get('M', 1)
    role = data.get('role', 'hider').lower()

    if N is None or role not in ('hider', 'seeker'):
        return jsonify({'error': 'Invalid input'}), 400

    current_player = u.PLAYER.HIDER if role == 'hider' else u.PLAYER.SEEKER
    game = Game(N=N, M=M)
    hider_prob, seeker_prob = game.get_probabilties()

    return jsonify({
        'message': f'Game created with {N} columns and role: {role}',
        'world': [[cell.value for cell in row] for row in game.world],
        'payoff_matrix': game.get_payoff_matrix().tolist(),
        'hider_prob': hider_prob.tolist(),
        'seeker_prob': seeker_prob.tolist(),
    })


@app.route('/round', methods=['POST'])
def play_round():
    if not game:
        return jsonify({'error': 'Game not initialized'}), 400
    data = request.get_json()
    player_type_str = data.get('player_type')
    is_optimal = data.get('is_optimal', False)
    print(player_type_str.upper())
    try:
        player_type = u.PLAYER[player_type_str.upper()]
    except KeyError:
        return jsonify({'error': 'Invalid player_type'}), 400

    if is_optimal:
        move = game.play_optimal(player_type)
    else:
        move = game.play_random()
    print(move)
    return jsonify({
        'move': move,
    })



@app.route('/simulate', methods=['POST'])
def simulate_game():
    from simulation import simulate  

    if game is None:
        return jsonify({'error': 'Game not initialized'}), 400

    data = request.get_json()
    is_optimal = data.get('is_optimal', True) 
    moves, scores, rounds_won = simulate(game, rounds=100, is_optimal=is_optimal)

    return jsonify({
        'moves': moves,
        'scores': scores,
        'rounds_won': rounds_won,
    })

if __name__ == '__main__':
    app.run(debug=True)
