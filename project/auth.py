
from typing import KeysView
from flask import Blueprint,Flask, render_template, redirect, url_for, request, flash, g
from flask_sqlalchemy import *
from sqlalchemy.sql.operators import from_
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Mission
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from os import *
import sys
from sqlalchemy import select, or_
from sqlalchemy import *
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session
from sqlalchemy.inspection import inspect
import feedparser
from flask_socketio import SocketIO, send



'''
Notre application utilisera le modèle d'usine de l'application Flask avec des plans. 
Nous aurons un modèle qui gère tout ce qui est lié à la propriété auth, 
et nous en aurons un autre pour nos itinéraires réguliers, 
qui comprennent l'index et la page de profil protégé.
'''

auth = Blueprint('auth', __name__)

Feed_URL="https://www.france24.com/fr/d%C3%A9couvertes/rss"
app = Flask(__name__)


@auth.route('/profile')
def profile():
    
    mission_opt=db.session.query(Mission.mission).filter_by(id_ex_user=current_user.id).all()
    
    return render_template('salon.html',name=current_user.username, posts=mission_opt)



@auth.route('/login')
def login():
    return render_template('Login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')
 

@auth.route('/Recherche', methods=['GET','POST'])
def recherche():
    
    if request.method == 'POST':
        mapper = inspect(Mission)
        fore=request.form #ceci marche mais il faut des ajustements
        search_value=fore['search']
        search="{}".format(search_value) # j'ai retirer % attention on sais jms
        name=current_user.username
    
        results=Mission.query.filter(Mission.mission.like(search))

        return render_template('Recherche.html', missions=results, name=current_user)
    else:
        print('cela ne marche pas')
        return render_template('Recherche.html', name=current_user.username)
    
    




@auth.route('/signup', methods=['POST'])
def signup_post():
        # code to validate and add user to database goes here
        username=request.form.get('username')
        #lastname=request.form.get('lastname')
        password=request.form.get('password')
        email=request.form.get('email')
        
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
       
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'), email=email)# j'ai enlever , lastname=lastname
        #print(User)
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()
        
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')    
            return redirect(url_for('auth.signup'))
    
        return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email=request.form.get('email')
    password=request.form.get('password')
    remember= True if request.form.get('remember_me') else False
    
    user= User.query.filter_by(email=email).first()
    
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('SVP regarder votre login en details et reesayer')
        return redirect(url_for('auth.login'))# if the user doesn't exist or password is wrong, reload the page
    
     # if the above check passes, then we know the user has the right credentials
    
    login_user(user, remember=remember)
    
    # if the above check passes, then we know the user has the right credentials
    return redirect(url_for('main.profile'))
        
        

@auth.route('/logout')
@login_required #Enfin, nous avons ajouté l'autorisation à notre app en utilisant le décorateur @login_required sur une page de profil afin que seuls les utilisateurs connectés puissent voir cette page.
def logout():
    logout_user()
    return redirect(url_for('main.index'))



@auth.route('/depots/', methods=['GET', 'POST'])
@login_required
def depots_mission():
    if request.method == 'POST':
        mission_o=request.form.get('option')
        user_id=current_user.id
        text_details=request.form.get('details')
        print('POST')
        
    
        new_p= Mission(id_ex_user=user_id, mission=mission_o, text=text_details)
        
        db.session.add(new_p)
        db.session.commit()
        
   
        return redirect(url_for('auth.profile'))
    
    elif request.method == 'GET':
        print('GET')
        return render_template('depots.html', name=current_user.username)

    return render_template('salon.html', name=current_user.username)


    



  


    
    
   




