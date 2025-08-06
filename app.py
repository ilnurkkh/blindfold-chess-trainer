from flask import Flask, render_template, request, redirect, jsonify
from models import db, Game
import chess
import chess.pgn
import random

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True # Reloads server everytime code is 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Connect db to this Flask app
db.init_app(app)

# Create database tables if not exist
with app.app_context():
    db.create_all()

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
                    pgn = get_pgn_string()
                    result = '1/2-1/2'  # Draw result
                    new_game = Game(mode="self", moves=pgn, result=result)
                    db.session.add(new_game)
                    db.session.commit()
                    return render_template('result.html', result=result, pgn=pgn)
                else:
                    return render_template('index.html', turn=turn, error="Draw cannot be claimed now.")
            
            elif 'resign' in request.form: # If Resign button is pressed
                game_over = True
                result = '0-1' if board.turn == chess.WHITE else '1-0' # Determine result based on whose turn it is
                pgn = get_pgn_string()
                new_game = Game(mode="self", moves=pgn, result=result)
                db.session.add(new_game)
                db.session.commit()
                return render_template('result.html', result=result, pgn=pgn)
            
            elif 'agree_draw' in request.form: # If Agree Draw button is pressed
                game_over = True
                pgn = get_pgn_string()
                result = '1/2-1/2'  # Draw result
                new_game = Game(mode="self", moves=pgn, result=result)
                db.session.add(new_game)
                db.session.commit()
                return render_template('result.html', result='1/2-1/2', pgn=pgn)
    
            # Makes the move on the board
            try:
                move = board.parse_san(request.form.get('move'))
                board.push(move)
                game_over = board.is_game_over()
                return redirect('/')
            except ValueError:
                # If the move is invalid, render the same page with an error message
                return render_template('index.html', turn=turn, error="Invalid move. Please try again.")

        if request.args.get("from", None) == "clear": # If visited from other pages, clear the game state
            board.reset()  # Reset the chess board
            return render_template('index.html', turn='White')
        
        return render_template('index.html', turn=turn)
    
    # Restart game if it is over
    if request.method == 'POST':
        game_over = False
        board.reset()
        return render_template('index.html', turn="White")

    # Game is over, render the result
    from_page = request.args.get("from", None)  # read ?from=...
    if from_page == "clear":
        return render_template('index.html', turn="White")
    else:
        game_over = True
        pgn = get_pgn_string()
        result = board.result()
        new_game = Game(mode="self", moves=pgn, result=result)
        db.session.add(new_game)
        db.session.commit()
        return render_template('result.html', result=result, pgn=pgn)


@app.route('/choose_color', methods=['GET', 'POST'])
def choose_color():

    global game_over
    game_over = False  # Reset game state when choosing color
    board.reset()  # Reset the chess board

    return render_template('color.html')
    

@app.route('/play_the_computer', methods=['GET', 'POST'])
def play_the_computer():
    
    global game_over

    comp_white = None

    while not game_over:

        if request.method == 'POST':

            if 'claim_draw' in request.form: # If Claim Draw button is pressed
                if board.can_claim_fifty_moves() or board.can_claim_threefold_repetition(): # Check if draw can be claimed
                    game_over = True
                    pgn = get_pgn_string()
                    result = '1/2-1/2'  # Draw result
                    new_game = Game(mode="computer", moves=pgn, result=result)
                    db.session.add(new_game)
                    db.session.commit()
                    return render_template('result1.html', result=result, pgn=pgn)
                else:
                    return render_template('comp.html', error="Draw cannot be claimed now.")
            
            elif 'resign' in request.form: # If Resign button is pressed
                game_over = True
                result = '0-1' if board.turn == chess.WHITE else '1-0' # Determine result based on whose turn it is
                pgn = get_pgn_string()
                new_game = Game(mode="computer", moves=pgn, result=result)
                db.session.add(new_game)
                db.session.commit()
                return render_template('result1.html', result=result, pgn=pgn)

            elif 'white' in request.form:
                return render_template('comp.html', compmove=None)
            elif 'black' in request.form:
                move = random.choice(list(board.legal_moves))
                compmove_san = board.san(move)  # get SAN before pushing
                board.push(move)
                return render_template('comp.html', compmove=compmove_san)
            
            try:
                move = board.parse_san(request.form.get('move'))
                board.push(move)
                game_over = board.is_game_over()
                return redirect('/play_the_computer')
            except ValueError:
                return render_template('comp.html', error="Invalid move. Please try again.")
            
        move = random.choice(list(board.legal_moves))
        move_san = board.san(move)
        board.push(move)
        game_over = board.is_game_over()
        if not game_over:
            return render_template('comp.html', compmove=move_san)
        else:
            return render_template('result.html', result=board.result(), pgn=get_pgn_string())
    
    return render_template('result1.html', result=board.result(), pgn=get_pgn_string())

@app.route("/validate_move", methods=["POST"])
def validate_move():
    move_text = request.json.get("move", "").strip()
    temp_board = board.copy()

    try:
        temp_board.parse_san(move_text)
        return jsonify(valid=True)
    except ValueError:
        return jsonify(valid=False)
    
@app.route('/history')
def history():
    games = Game.query.order_by(Game.date_played.desc()).all()
    return render_template("history.html", games=games)
        
if __name__ == '__main__':
    app.run(debug=True)