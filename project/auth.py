from typing import KeysView
from flask import Blueprint, Flask, render_template, redirect, url_for, request, flash, g
from flask_sqlalchemy import *
from sqlalchemy.sql.operators import from_
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Mission
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from flask_login import LoginManager
from os import *
import sys
from sqlalchemy import select, or_
from sqlalchemy import *
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
import feedparser
from flask_socketio import SocketIO, send

auth = Blueprint('auth', __name__)

Feed_URL = "https://www.france24.com/fr/d%C3%A9couvertes/rss"
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)
with app.app_context():  #####cette parti est importante pour pouvoir crée la table et donc ne pas avoir de message derreu
    db.create_all()
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    mission_opt = db.session.query(Mission.mission).filter_by(id_ex_user=current_user.id).all()

    return render_template('salon.html', name=current_user.username, posts=mission_opt)


@app.route('/login')
def login():
    return render_template('Login.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/Recherche', methods=['GET', 'POST'])
def recherche():
    if request.method == 'POST':
        mapper = inspect(Mission)
        fore = request.form  # ceci marche mais il faut des ajustements
        search_value = fore['search']
        search = "{}".format(search_value)  # j'ai retirer % attention on sais jms
        name = current_user.username

        results = Mission.query.filter(Mission.mission.like(search))

        return render_template('Recherche.html', missions=results, name=current_user.username)
    else:
        print('cela ne marche pas')
        return render_template('Recherche.html', name=current_user.username)


@app.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    username = request.form.get('username')
    # lastname=request.form.get('lastname')
    password = request.form.get('password')
    email = request.form.get('email')

    user = User.query.filter_by(
        email=email)  # if this returns a user, then the email already exists in database
    if user is False:
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'),
                    email=email)  # j'ai enlever , lastname=lastname
        # print(User)
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
    else:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('login'))

    return redirect(url_for('login'))


@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember_me') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('SVP regarder votre login en details et reesayer')
        return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials

    login_user(user, remember=remember)

    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('profile'))


@app.route('/logout')
@login_required  # Enfin, nous avons ajouté l'autorisation à notre app en utilisant le décorateur @login_required sur
# une page de profil afin que seuls les utilisateurs connectés puissent voir cette page.
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/depots/', methods=['GET', 'POST'])
@login_required
def depots_mission():
    if request.method == 'POST':
        mission_o = request.form.get('option')
        user_id = current_user.id
        text_details = request.form.get('details')
        print('POST')

        new_p = Mission(id_ex_user=user_id, mission=mission_o, text=text_details)

        db.session.add(new_p)
        db.session.commit()

        return redirect(url_for('profile'))

    elif request.method == 'GET':
        print('GET')
        return render_template('depots.html', name=current_user.username)

    return render_template('salon.html', name=current_user.username)


if __name__ == '__main__':
    app.run(debug=True)
