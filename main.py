from flask import Flask, render_template, url_for, request, jsonify
from flask_bootstrap import Bootstrap5
from code_chars import MORSE_CODE_CHARS
from codes import APP_KEY, letters, numbers, symbols
import subprocess
import random


app = Flask(__name__)
app.config['SECRET_KEY'] = APP_KEY
Bootstrap5(app)

# Dictionary of available spaces for tic-tac-toe
boxes = {
    1: (0, 0),
    2: (1, 0),
    3: (2, 0),
    4: (0, 1),
    5: (1, 1),
    6: (2, 1),
    7: (0, 2),
    8: (1, 2),
    9: (2, 2),
}


# For morse code app
def convert_to_morse_code(plain_text):
    morse_code = ''
    for char in plain_text:
       if char == ' ':
            morse_code += ' / '
       else:
            morse_code += MORSE_CODE_CHARS[char.upper()] + ' '
    return morse_code


# To initialize the board for tic-tac-toe
def initialize_board():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]


# Initialize the box list for tic-tac-toe
def initialize_box_list():
    global box_list
    box_list = list(boxes.keys())


# Function to check winner in tic-tac-toe
def check_winner(player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True

    return False


# Function to check if board is full in tic-tac-toe
def is_board_full():
    return all(all(cell != ' ' for cell in row) for row in board)


# Function to get a random open space for the computer move in tac-tac-toe
def get_random_open_space():
    available_spaces = [key for key in box_list]
    return random.choice(available_spaces)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/morse_code', methods=['GET', 'POST'])
def morse_code():
    if request.method == 'POST':
        try:
            plain_text = request.form['plain_text']
            morse_code_output = convert_to_morse_code(plain_text)
            return render_template('morse_code.html', plain_text=plain_text, morse_code_output=morse_code_output)
        except subprocess.CalledProcessError as e:
            return f"Error running morse_code function: {e}"

        # Return the form if the request method is GET
    return render_template('morse_code.html')


@app.route('/tictactoe', methods=['GET', 'POST'])
def tictactoe():
    return render_template('tictactoe.html')


@app.route('/move', methods=['GET', 'POST'])  # Route for player to make move in tic-tac-toe
def move():
    current_player = 'X'

    row = int(request.args.get('row'))
    col = int(request.args.get('col'))
    value_received = (row, col)

    if value_received in boxes.values():
        key_to_remove = next((key for key, value in boxes.items() if value == value_received), None)
        if key_to_remove in box_list:
            box_list.remove(key_to_remove)
            board[row][col] = current_player

            # Check for a winner or a draw
            winner = check_winner(current_player)
            if winner:
                return jsonify(valid=True, message=f"Player wins!", winner=current_player, game_over=True)
            elif len(box_list) == 0:  # Check if board is full
                return jsonify(valid=True, message="It's a draw!", draw=True, game_over=True)

            return jsonify(valid=True, message="Valid move")

    return jsonify(valid=False, message="Invalid move")


@app.route('/computer_move', methods=['GET', 'POST'])  # Route for computer to make move in tic-tac-toe
def computer_move():
    # Get a random open space for the computer's move
    computer_move = get_random_open_space()
    computer_row, computer_col = boxes[computer_move]
    board[computer_row][computer_col] = 'O'
    box_list.remove(computer_move)  # Remove the computer's move from box_list

    # Check for a winner or a draw after computer's move
    winner = check_winner('O')
    if winner:
        return jsonify(valid=True, message=f"Computer wins!", winner='O')
    elif is_board_full():
        return jsonify(valid=True, message="It's a draw!", draw=True)

    return jsonify(valid=True, row=computer_row, col=computer_col)


@app.route('/reset', methods=['POST'])  # Route to allow 'Play Again' in tic-tac-toe
def reset_game():
    # variables to reset
    initialize_board()
    initialize_box_list()

    return jsonify(message="Game has been reset.")


@app.route('/app3', methods=['GET', 'POST'])  # Future app
def app3():
    return render_template('app3.html')


if __name__ == "__main__":
    initialize_board()    # Tic-Tac-Toe
    initialize_box_list()    # Tic-Tac-Toe
    app.run(host='127.0.0.1', port=5000)
