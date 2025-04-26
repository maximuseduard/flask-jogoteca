
from flask import render_template, request, redirect, session, flash, url_for
from jogoteca import app, db
from models import Jogos, Usuarios


@app.route('/')
def home():
    games = Jogos.query.order_by(Jogos.id)
    
    return render_template('list.html', title='Jogos', games=games)

@app.route('/new')
def new():
    if 'user' not in session or session['user'] == None:
        return redirect(url_for('login', next=url_for('new')))

    return render_template('new.html', title='Add game')

@app.route('/create', methods=['POST', ])
def create():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    game = Jogos.query.filter_by(nome=nome).first()

    if game:
        flash('Already exist!')
        return redirect(url_for('index'))

    new_game = Jogos(nome=nome, categoria=categoria, console=console)
    db.session.add(new_game)
    db.session.commit()

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
    user = Usuarios.query.filter_by(nickname=request.form['user']).first()
    if user:
        if request.form['senha'] == user.senha:
            session['user'] = user.nickname
            flash('Login succeeded!')
            nextPage = request.form['next']
            return redirect(nextPage)
    else:
        flash('Login failed. Try again.')
        return redirect(url_for('login'))