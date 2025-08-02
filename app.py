from flask import Flask, render_template, request, redirect
import chess

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

board = chess.Board()

@app.route('/', methods=['GET', 'POST'])
def index():

    while not board.is_game_over():
    
        if request.method == 'POST':
            # Handle form submission here
            move = chess.Move.from_uci(request.form.get('move'))
            if move in board.legal_moves:
                board.push(move)
                return redirect('/')
            else:
                return redirect('/')
            
        return render_template('index.html')
    
    return render_template('result.html', result=board.result())

if __name__ == '__main__':
    app.run(debug=True)