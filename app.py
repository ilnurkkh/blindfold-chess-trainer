from flask import Flask, render_template, request, redirect
import chess
import chess.pgn

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True # Reloads server everytime code is changed

board = chess.Board()

game_over = False # Initialising game state


def get_pgn_string(): # Returns game pgn in string format
    return str(chess.pgn.Game.from_board(board))


@app.route('/',  methods=['GET', 'POST'])
def index():

    global game_over

    while not game_over:

        turn = "White" if board.turn == chess.WHITE else "Black" # Determine whose turn it is
    
        if request.method == 'POST':
    
            if 'claim_draw' in request.form: # If Claim Draw button is pressed
                if board.can_claim_fifty_moves() or board.can_claim_threefold_repetition(): # Check if draw can be claimed
                    game_over = True
                    return render_template('result.html', result='1/2-1/2', pgn=get_pgn_string())
                else:
                    return render_template('index.html', turn=turn, error="Draw cannot be claimed now.")
    
            # Makes the move on the board
            try:
                move = board.parse_san(request.form.get('move'))
                board.push(move)
                game_over = board.is_game_over()
                return redirect('/')
            except ValueError:
                # If the move is invalid, render the same page with an error message
                return render_template('index.html', turn=turn, error="Invalid move. Please try again.")

        # Starts Game  
        return render_template('index.html', turn=turn)
    
    # Restart game if it is over
    if request.method == 'POST':
        game_over = False
        board.reset()
        return render_template('index.html', turn="White")

    # Game is over, render the result
    game_over = True
    return render_template('result.html', result=board.result(), pgn=get_pgn_string())

if __name__ == '__main__':
    app.run(debug=True)