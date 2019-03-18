from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
# from collections import defaultdict, setdefault
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import NoResultFound

import pymysql
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Venu0p@l@localhost/TeamPlayer'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Venug0p@l@localhost:3306/TeamPlayer'
db = SQLAlchemy(app)

class Team(db.Model):
    __tablename__ = 'Team' 
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(80))
    team_image = db.Column(db.BLOB)

    def __repr__(self):
        return "<Team(team_name='%s', team_id='%s, team_image='%s')>" % (
                                self.team_name, self.team_id, self.team_image)


class Player(db.Model):
    """docstring for Player"""
    __tablename__ = 'player'
    player_id = db.Column(db.Integer, primary_key=True)
    player_fname = db.Column(db.String(80))
    player_lname = db.Column(db.String(80))
    player_image = db.Column(db.BLOB)
    team_id = db.Column(db.Integer, db.ForeignKey('Team.team_id'))

    def __repr__(self):
        return "<Team(player_fname='%s', player_id='%s, team_id='%s)>" % (
                                self.player_fname, self.player_id, self.team_id)
        
@app.route('/')
def home():
    return render_template('login.html')


@app.route('/detail', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        teams = get_team()
        if teams:
            return render_template('team-players.html', teams=teams)
        else:
            return render_template('team-players.html')
    else:
        flash('Invalid username or password. Please try again!')
        return render_template('login.html')


@app.route('/teamplayer', methods=['POST'])
def add_team_player():
    if request.form['add_team_play'] == 'Add Team':
        return render_template('addteam.html')
    elif request.form['add_player_play'] == 'Add Player':
        teams = get_team()
        return render_template('addplayer.html', teams=teams)
    else:
        import pdb; pdb.set_trace()
        players = Player.query.all()
        return render_template('viewplayers.html', players=players)

# @app.route('/viewplayer', methos=['GET'])
# def view_players():
#     players = Team.query.all()
#     return render_template('viewplayers.html', players=players)

@app.route('/addteam', methods=['POST', 'GET'])
def add_team():
    if request.method == 'POST':
        result = request.form
        team = Team.query.filter_by(team_name=result['team_name']).first()
        if not team:
            with open(result['file'], 'rb') as file:
                Image_binaryData = file.read()
            team1 = Team(team_name=result['team_name'],team_image=Image_binaryData)
            db.session.add(team1)
            db.session.commit()
            flash(result['team_name'] + ' is added successfully')
            teams = get_team()
            return render_template('team-players.html', teams=teams)
        else:
            flash(result['team_name'] + ' is already present')
            return render_template('addteam.html')


@app.route('/player_information', methods = ['POST', 'GET'])
def player_information():
    if request.method == 'POST':
        result = request.form
        player = Player(player_fname=result['player_first_name'], player_lname=result['player_last_name'], team_id=result['team_selected'])
        db.session.add(player)
        db.session.commit()
        teams = get_team()
        if teams:
            return render_template('team-players.html', teams=teams)
        else:
            return render_template('team-players.html')

def get_team():
    teams = Team.query.all()
    return teams


@app.route('/edit_team/<int:team_id>', methods=['POST', 'GET', 'PUT'])
def team_edit(team_id):
    if request.method == 'GET':
        team = Team.query.filter_by(team_id=team_id).one()
        return render_template('edit_team.html', team=team)


@app.route('/update_team', methods=['POST', 'GET'])
def updateteam():
    if request.method == 'POST':
        result = request.form
        team = Team.query.filter_by(team_id=result.get('team_id')).one()
        team.team_name = result.get('team_name')
        db.session.commit()
        teams = get_team()
        if teams:
            return render_template('team-players.html', teams=teams)

@app.route('/deleteTeam/<int:team_id>', methods=['POST', 'GET'])
def delete_team(team_id):
    if request.method == 'GET':
        Team.query.filter_by(team_id=team_id).delete()
        db.session.commit()
        teams = get_team()
        if teams:
            return render_template('team-players.html', teams=teams)
        else:
            return render_template('team-players.html')

app.secret_key = os.urandom(24)
app.run()
