from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo

# app initailization
app = Flask(__name__)
app.secret_key = 'secretkey'

# database path
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/dbtest"
mongo = PyMongo(app)

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

# checks if the user is authenticate user or not
@app.route('/login', methods=['POST'])
def findEmp():
    usr = request.form['username']
    pwd = request.form['pwd']

    if usr and pwd:
        id = mongo.db.employee.find(
            {'username': usr, 'password': pwd}, {'pwd': 0})
        temp = 0
        for i in id:
            temp += 1
        if temp:
            session['username'] = 'auth'
            return redirect(url_for('goToOptions'))
        else:
            return not_found()
    else:
        return not_found()

# inserts new user in the database
@app.route('/signup', methods=['POST'])
def createEmp():
    usr = request.form['username']
    pwd = request.form['pwd']
    role = request.form['role']

    if usr and pwd and role:
        id = mongo.db.employee.insert(
            {'username': usr, 'password': pwd, 'role': role})
        session['username'] = 'auth'
        return redirect(url_for('goToOptions'))
    else:
        return not_found()


@app.route('/options')
def goToOptions():
    if 'username' in session:
        if session['username'] == 'auth':
            return render_template("options.html")
        else:
            return not_found()
    else:
        return not_found()


@app.route('/createCust.html')
def createCust():
    if 'username' in session:
        if session['username'] == 'auth':
            return render_template("createCust.html")
        else:
            return not_found()
    else:
        return not_found()


@app.route('/updateCust.html')
def updateCust():
    if 'username' in session:
        if session['username'] == 'auth':
            return render_template("updateInit.html")
        else:
            return not_found()
    else:
        return not_found()


@app.route('/delCust.html')
def delCust():
    if 'username' in session:
        if session['username'] == 'auth':
            return render_template("delCust.html")
        else:
            return not_found()
    else:
        return not_found()


@app.route('/crud/<id>', methods=['GET', 'POST', 'DELETE'])
def crudCust(id):
    if id == 'create':
        return 'hello'
    elif id == 'update':
        return request.form['ssnid']
    elif id == 'delete':
        return 'delete'
    elif id == "fetchCust":
        return render_template('updateCust.html', a='1234', b='shlok', c='mumbai', d='18')
    else:
        return not_found()


if __name__ == '__main__':
    app.run(debug=True)
