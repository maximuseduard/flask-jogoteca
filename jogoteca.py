from flask import Flask, render_template, request, redirect, session, flash, url_for

class Game:
    def __init__(self, name, category, console):
        self.name = name
        self.category = category
        self.console = console

game1 = Game('Tetris', 'Puzzle', 'Atari')
game2 = Game('Skyrim', 'RPG', 'Xbox')
game3 = Game('Crash', 'Racing', 'PS2')

gameList = [game1, game2, game3]

class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password
        
user1 = User("Bruno", "BD", "12345")
user2 = User("John", "Big", "12345")
user3 = User("Mary", "Cake", "12345")

users = { user1.nickname : user1, 
          user2.nickname : user2,
          user3.nickname : user3 }

app = Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def home():
    if 'user' not in session or session['user'] == None:
        return redirect(url_for('login'))

    return render_template('list.html', title='Games', games = gameList)

@app.route('/new')
def new():
    if 'user' not in session or session['user'] == None:
        return redirect(url_for('login', next=url_for('new')))

    return render_template('new.html', title='Add game')

@app.route('/create', methods=['POST', ])
def create():
    name = request.form['name']
    category = request.form['category']
    console = request.form['console']
    game = Game(name, category, console)

    gameList.append(game)

    return redirect(url_for('home'))

@app.route('/login')
def login():
    next = request.args.get('next')

    return render_template('login.html', next=next)

@app.route('/logout')
def logout():
    session['user'] = None
    flash('Logout succeeded!')
    return redirect(url_for('home'))

@app.route('/auth', methods=['POST', ])
def auth():
    if request.form['user'] in users:
        user = users[request.form['user']]

        if request.form['password'] == user.password:
            session['user'] = user.nickname
            flash('Login succeeded!')
            nextPage = request.form['next']
            
            return redirect(nextPage)
    else:
        flash('Login failed. Try again.')
        
        return redirect(url_for('login'))

app.run(debug=True)