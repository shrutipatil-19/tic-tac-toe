from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
winner = None

def check_winner():
    global winner
    lines = []

    # Rows and Columns
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])

    # Diagonals
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line == ["X", "X", "X"]:
            winner = "X"
            return
        if line == ["O", "O", "O"]:
            winner = "O"
            return

    if all(cell != "" for row in board for cell in row):
        winner = "Draw"

@app.route("/board", methods=["GET"])
def get_board():
    return jsonify({"board": board, "player": current_player, "winner": winner})

@app.route("/move", methods=["POST"])
def make_move():
    global current_player
    if winner:
        return jsonify({"error": "Game over"}), 400

    data = request.get_json()
    row, col = data["row"], data["col"]

    if board[row][col] != "":
        return jsonify({"error": "Cell already taken"}), 400

    board[row][col] = current_player
    check_winner()

    if not winner:
        current_player = "O" if current_player == "X" else "X"

    return jsonify({"board": board, "player": current_player, "winner": winner})

@app.route("/reset", methods=["POST"])
def reset_game():
    global board, current_player, winner
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    winner = None
    return jsonify({"message": "Game reset"})

if __name__ == "__main__":
    app.run(debug=True)
