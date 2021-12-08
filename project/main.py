from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Mission
from . import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


main = Blueprint('main', __name__)

app = Flask(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required # Enfin, nous avons ajouté l'autorisation à notre app en utilisant le décorateur @login_required sur une page de profil afin que seuls les utilisateurs connectés puissent voir cette page.
def profile():
    return render_template('salon.html', name=current_user.username)

@main.route('/login')
def login():
    return render_template('Login.html')

'''
@main.route('/depots', methods=['GET', 'POST'])
@login_required
def depots():
    
    if request.method == 'POST':
        rrr=request.args.get('option')
        personne=current_user.username
        
    
        new_p= Mission(id_ex_user=personne, mission=rrr)
    
    
        db.session.add(new_p)
        db.session.commit()
    
    
    
    return render_template('salon.html')


@main.route('/depots')
def depots_mission():
    return render_template('depots.html')
'''     

