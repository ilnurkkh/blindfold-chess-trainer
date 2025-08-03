from flask import Flask, render_template, request, redirect
import chess
import chess.pgn

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

board = chess.Board()

def get_pgn_string():

    # Returns game pgn in string format
    return str(chess.pgn.Game.from_board(board))

@app.route('/', methods=['GET', 'POST'])
def index():

    while not board.is_game_over():

        turn = "White" if board.turn == chess.WHITE else "Black"
    
        if request.method == 'POST':
            # Makes the move on the board
            try:
                move = board.parse_san(request.form.get('move'))
                board.push(move)
                return redirect('/')
            except ValueError:
                # If the move is invalid, render the same page with an error message
                return render_template('index.html', turn=turn, error="Invalid move. Please try again.")
            
        return render_template('index.html', turn=turn)
    
    # Restart game if it is over
    if request.method == 'POST':
        board.reset()
        return render_template('index.html', turn="White")

    # Game is over, render the result
    return render_template('result.html', result=board.result(), pgn=get_pgn_string())

if __name__ == '__main__':
    app.run(debug=True)