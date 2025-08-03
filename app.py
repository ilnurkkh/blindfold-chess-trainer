from flask import Flask, render_template, request, redirect
import chess

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

board = chess.Board()

@app.route('/', methods=['GET', 'POST'])
def index():

    while not board.is_game_over():

        turn = "White" if board.turn == chess.WHITE else "Black"
    
        if request.method == 'POST':
            # Makes the move on the board
            move = board.parse_san(request.form.get('move'))
            board.push(move)
            return redirect('/')
            
        return render_template('index.html', turn=turn)
    
    # Restart game if it is over
    if request.method == 'POST':
        board.reset()
        return render_template('index.html', turn="White")

    # Game is over, render the result
    return render_template('result.html', result=board.result())

if __name__ == '__main__':
    app.run(debug=True)