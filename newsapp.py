import re
from flask import Flask, render_template, request, redirect, url_for, flash,session
from datetime import datetime
from flaskext.mysql import MySQL
from passlib.hash import sha256_crypt

# create instance of the Flask class
# here parameter of Flask constructor is give current module's name
app = Flask(__name__)

mysql = MySQL()
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flask_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
# display current time
today = datetime.now()
print (today.strftime("%Y - %m - %d  %H : %M : %S"))

#here decorator is used to navigate the URL
# whenever user go to the home page route function fire the register mandatory function and return the data
@app.route("/")
def reg_mand():
    # passing reference of date variable
    return render_template("register.html",today=today)

# register page
@app.route("/register/",methods=['GET','POST'])
def register():
    msg=""
    # check if request is post or not
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # create hashed password
        hashed = sha256_crypt.encrypt(str(password))

        # connect with the database
        conn = mysql.connect()
        # create cursor for connection
        cursor = conn.cursor()

        # Check if account exists in database or not
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))

        # fetch that user
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg='Account already exists!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'

        # regular expression
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', username):
            msg = 'Username must contain only characters!'

        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (null,%s, %s, %s)', (username, email,hashed))
            # commit all changes
            conn.commit()
            # after all
            conn.close()
            cursor.close()
            msg = 'You have successfully registered!'
            return redirect(url_for('login',msg=msg))
    return render_template('register.html', msg=msg)
# Login page
@app.route("/login/",methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        userpass = request.form['password']
        conn = mysql.connect()
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM users WHERE username = %s",[username])
        # Fetch one record and return result

        if result > 0:
            data = cursor.fetchone()
            # retrieve password from database
            password = data[3]
            # retrieve id
            id_num = data[0]

            # match both hased and user password
            if sha256_crypt.verify(userpass, password):

                # if true session will be started
                session['loggedin'] = True
                session['admin'] = False

                # store user in session
                session['username'] = username
                session['id'] = id_num
                msg='Logged In Successfully!!!', 'success'
                return redirect(url_for('home',msg=msg))
            else:
                msg = 'Invalid Login'
                return render_template('login.html',msg=msg)
        else:
            msg='User not found'
            return render_template('login.html',msg=msg)

    return render_template('login.html',msg=msg)


@app.route("/home/")
def home():
    # first check if user is logged in or not
    if 'loggedin' in session:
        # if true it render the request to particular destination
        return render_template("index.html",username=session['username'],today=today)
    # if not logged in redirect to login page
    return redirect(url_for('login'))


# news page
@app.route("/news/",methods = ['GET','POST'])
def news():
    msg=''
    if 'loggedin' in session:
        if request.method == 'POST' and 'headlines' in request.form and 'description' in request.form and 'author' in request.form and 'category' in request.form:
            headlines  = request.form['headlines']
            description = request.form['description']
            author = request.form['author']
            category = request.form['category']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("INSERT into news(headlines,description,author,category) VALUES (%s, %s, %s, %s)", (headlines,description,author,category))
            # print('headlines : {0} :::: description : {1} :::: author : {2} :::: category : {3}'.format(headlines,description,author,category))
            conn.commit()
            msg = "News Added Successfully"
            # print(cursor.fetchall())
            cursor.close()
            return redirect(url_for('shownews',msg=msg))
        else:
            msg="Something went wrong please try again"
            return render_template("news.html",today=today,msg=msg)
    return redirect(url_for('login'))

# show news
@app.route("/shownews/",methods = ['GET','POST'])
def shownews():
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM news')
        rows = cursor.fetchall()
        # print(rows)
        return render_template("shownews.html", rows=rows, today=today)
    return redirect(url_for('login'))
    # con = sqlite3.connect("news.db")
    # con.row_factory = sqlite3.Row

    # cur = con.cursor()
    # cur.execute("select * from news")
    #
    # rows = cur.fetchall()



# contact page
@app.route("/contact/",methods = ['GET','POST'])
def contact():
    msg=""
    if 'loggedin' in session:
        if request.method == 'POST' and 'fullname' in request.form and 'email' in request.form and 'heading' in request.form and 'subject' in request.form:
            name  = request.form['fullname']
            email = request.form['email']
            heading = request.form['heading']
            subject = request.form['subject']
            conn = mysql.connect()
            cursor = conn.cursor()

            # with sqlite3.connect("news.db") as con:
            #     cur = con.cursor()
            cursor.execute("INSERT into contact(name,email,heading,subject) VALUES (%s, %s, %s, %s)", (name,email,heading,subject))
            print('name : {0} :::: email : {1} :::: heading : {2} :::: subject : {3}'.format(name,email,heading,subject))
            conn.commit()

            print(cursor.fetchall())
            msg = "Your Query Successfully Registered"
            cursor.close()

        return render_template("contact.html",today=today,msg=msg)
    return redirect(url_for('login'))


@app.route("/editnews/<id>",methods = ['GET','POST'])

def edit(id):
    try:
        print("asdadasdasdadd : "+id)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * from news where id = %s",(id,))
        # print('id:{0}'.format(id))
        data=cursor.fetchone()
        print(data)
        cursor.close()
        return render_template('updatenews.html',data=data,today=today)
    except Exception as e:
        print(e)

@app.route("/updatenews/<id>",methods = ['GET','POST'])
def update(id):
    if 'loggedin' in session:
        try:
            print("update id"+id)
            
            headlines = request.form['headlines']
            print("headline",headlines)
            description = request.form['description']
            author = request.form['author']
            category = request.form['category']
            print('headlines : {0} :::: description : {1} :::: author : {2} :::: category : {3}'.format(headlines,description,author,category))
            print("updatesasdsa id"+id)
            if headlines and description and author and category:
                print('CorrectCorrectCorrectCorrectCorrect******************')
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute('Update news set headlines = %s, description = %s, author = %s, category = %s WHERE id = %s',(headlines,description,author,category,id))
                flash("News Updated Successfully")
                conn.commit()
                rows=cursor.fetchall()
                cursor.close()
                conn.close()
                return redirect(url_for('shownews',))
            else:
                msg="Somethong went wrong"
                print('*-----------InCorrectCorrectCorrectCorrectCorrect******************')
                return render_template('updatenews.html',msg=msg)
        except Exception as e:
            print(e)
    return redirect(url_for('login'))


@app.route("/delete/<id>")
def delete(id):
    try:
        print('id:{0}'.format(id))
        conn = mysql.connect()
        cursor = conn.cursor()
        result=cursor.execute("DELETE FROM news WHERE id=%s", (id,))
        print("Res : ",result)
        cursor.fetchone()
        conn.commit()
        conn.close()
        flash('User deleted successfully!')
        return redirect(url_for('shownews',))
    except Exception as e:
        print(e)



# logout
@app.route('/logout/')
def logout():
	session.pop('username', None)
	return redirect('/')



if __name__ == "__main__":
    #we need to run our flask app using .run funtion
    #if we don't want run everytime pass the debug = True
    # it will refresh everytime whenever changes is done
    app.secret_key = 'SECRET KEY'
    
    app.run(debug=True)


