from flask import Flask, jsonify, render_template, request, session, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from _datetime import datetime


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
import models
migrate = Migrate(app, db)


# index page
@app.route('/')
def index():
    return render_template('index.html')

# errorhandler
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/logout')
def logoutUser():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/login.html')
def indexLogin():
    return render_template('login.html')


@app.route('/signup.html')
def indexSignup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def createEmp():
    usr = request.form['username']
    pwd = request.form['pwd']
    role = request.form['role']

    if usr and pwd and role:
        user=models.User.query.filter_by(username=usr).first()
        if(user==None):
            user = models.User(username=usr,
                                role_id=role)
            user.set_password(pwd)

            # add employee to the database
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered! You may now login.')
            return redirect(url_for('indexLogin'))
    return not_found()
#
    # user = models.User.query.filter_by(username=usr).first()
    


if __name__ == '__main__':
    app.run(debug=True)