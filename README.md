# Blindfold Chess Trainer
#### Video Demo:  <https://youtu.be/CcJ2lc5Ln2w>
#### Description:
A web-app based blindfold chess trainer built for Harvard’s CS50 final project. Designed to help players practice and improve their visualization and memory by playing chess without a visible board.
Blindfold chess is not any new invention. It is quite a common thing in the chess world where chess masters, demonstrate their skills by playing their opponent blindfold without an actual board or anything to look at and they still win. Great chess players can visualise entire games in their head and visualisation is a crucial skill that every chess player has to train.

This project is a web-app built using flask and pure HTML, CSS and JavaScript.
There are two modes:-
- Play Yourself:- Here, player has to input both white's and black's moves
- Play with Computer:- Here, player can play against computer generated moves.

## Frontend

### HTML

- `index.html` Main landing page. This contains the section where you can play against yourself. It has an input section, where you have to input the algebraic notation of the move you wish to play. After inputting the move, the Play button has to be pressed. If the move is legal and valid, it will proceed, otherwise, an error message will be displayed. At any point in time, you can resign by clicking on the red flag button, or agree to a draw using the handshake button. (In case two players are playing using the same system). There is a claim draw option, which a user can press if they think they are eligible for a *threefold repetition* or *50 move rule*. If the button is pressed when none of the condition hold, an error message is displayed.
> Algebraic Notation is the standard way to record chess moves. Each move is written as the piece’s letter (omitted for pawns) followed by the destination square (e.g., Nf3 means knight to f3, e4 means pawn to e4). Special cases include captures (x), checks (+), checkmate (#), castling (O-O or O-O-O), and pawn promotions (e8=Q).

- `comp.html` It is the page where you can play against the computer. Once you have chosen your color on `color.html`, a screen similar to `index.html` will be displayed, where after each of your moves, the move computer played will be displayed. Also, agreeing to draw option is unavailable, of course.

- `color.html` When you try playing against the computer, you will first be greeted by this page where you can choose the color you'll be playing. After that you will be moved to `comp.html`.

- `result.html`/`result1.html` After a game ends, the result page will be displayed along with the PGN of the game.
> PGN (Portable Game Notation) is a plain-text format for recording chess games, including move history in algebraic notation and optional metadata like players, event, date, and result.

- `history.html` Each finished game gets saved in a database, and the content of the database is displayed on this page, including game info, result, date and time, and the PGN info.

Each of these HTML pages are nicely connected through the navbar at the top of each page. There is also a nice favicon of the black pawn emoji

### CSS
At first, I thought I'd use some CSS framework like Bootstrap or Tailwind, so I won't have to worry about the design part and could just focus on logic. But later I changed my mind and decided to use pure CSS. It was a hassle, but after learning about flexbox and some other CSS techniques, I was able to make my pages look decent enough.

- `style.css` This is the main stylesheet that contains the design elements. The navbar items show cool effects when hovered over them.

- `history.css` This stylesheet is specifically for the game history page

- `responsive.css` This stylesheet contains some media queries to make the webpages more responsive. When I saw how my webpage looks on smaller devices, the background didn't fit properly and sometimes the texts in input or buttons weren't properly readable or centered. To fix the background issue, I removed the background image and replaced it with a simple background color for smaller screens. In smaller screens, I also changed the display to none for some elements that weren't necessary like the history page. I tried my best to make the pages as responsive as I could using pure CSS.

### JS

- `script.js` This is the only JavaScript file, and the purpose of the code inside is to live check the user's input. If the current text in the input is a legal move, the border of the input area turns green, otherwise it turns red. This way the user doesn't have to play the move to know whether it is valid or not and can simply know it live while typing. I wanted to add more JavaScript features. For example, I thought of adding a toggle button where the user can sneak peek the current board position. But while trying to implement it, I thought it is against the spirit of blindfold chess, hence I dropped the idea. Perhaps in the future I will implement it but with the idea of having a limited number of hints type feature. For instance, in a game, someone can sneak peek maximum 3 times.

## Backend

### Python (Flask)

- `app.py` The main application that runs most of the backend tasks.
    - **Game Logic**: Uses the `python-chess` library to manage chess rules, moves, and game state
    - **Routes**: Provides routes for playing solo, playing against computer, choosing color, validating moves, and viewing game history
    - **Draw and Resign Handling**: Supports claiming draws (including threefold repetion and fifty-move-rule), resigning, and agreeing to draws.
    - **Move Validation**: Validates user moves and provides feedback for invalid moves.
    - **Templates**: Renders dynamic HTML pages using Flask's template engine
This file ties together the backend logic, database operations, and user interface, making it the core of the Blindfold Chess Trainer application.

- `models.py` Contains the database models for the project. These models define how data is stored, including the tables, columns, and relationships, and provide an easy way to interact with the database from the code. Uses SQLAlchemy to handle SQL queries for the database. All the finished games are stored in `games.db`.
