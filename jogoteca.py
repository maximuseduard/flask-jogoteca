from flask import Flask, render_template

class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

app = Flask(__name__)

@app.route('/home')
def ola():
    game1 = Game('Tetris', 'Puzzle', 'Atari')
    game2 = Game('Skyrim', 'RPG', 'Xbox')
    game3 = Game('Crash', 'Racing', 'PS2')

    gameList = [game1, game2, game3]
     
    return render_template('list.html', title='Games', games = gameList)

app.run()