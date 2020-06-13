from flask import Flask, jsonify, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/dbtest"

mongo = PyMongo(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'not found' + request.url
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.route('/login.html')
def indexLogin():
    return render_template('login.html')


@app.route('/signup.html')
def indexSignup():
    return render_template('signup.html')


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
            return render_template("options.html", msg="user found")
        else:
            return not_found()
    else:
        return not_found()


@app.route('/signup', methods=['POST'])
def createEmp():
    usr = request.form['username']
    pwd = request.form['pwd']
    role = request.form['role']

    if usr and pwd and role:
        id = mongo.db.employee.insert(
            {'username': usr, 'password': pwd, 'role': role})
        return render_template("options.html", msg="user found")
    else:
        return not_found()


if __name__ == '__main__':
    app.run(debug=True)
