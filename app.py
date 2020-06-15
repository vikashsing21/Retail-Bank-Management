from flask import Flask, jsonify, render_template, request, session, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from _datetime import datetime
import json

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
import models
migrate = Migrate(app, db)

# index page
@app.route('/')
def login():
    if session.get('username') and session.get('type')=='executive':
            return redirect('/customer')
    elif session.get('username') and session.get('type')=='cashier':
            return redirect('/cashier') 
    else:
        return render_template('login.html')


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
def logout():
    session.pop('username', None)
    session.pop('type', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        usr = request.form['username']
        pwd = request.form['password']
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
                flash('You have successfully registered! You may now login.','success')
                return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def findUser():
    if request.method=='POST':
        usr = request.form['username']
        pwd = request.form['password']
        if usr and pwd:
            user=models.User.query.filter_by(username=usr).first()
            if(user!=None and user.verify_password(pwd)):
                #in order to save most recent login time
                user.login=datetime.now()
                db.session.commit()
                session['username'] = usr
                if(user.role_id==1):
                    session['type']='cashier'    
                elif(user.role_id==0):                
                    session['type']='executive'
            else:
                flash("Given username and password Combinations doesn't match!","danger")
    return redirect(url_for('login'))
   



#==========Customers=========================
@app.route('/customer')
def customerIndex():
    if session.get('username') and session.get('type')=='executive':
            return render_template('Customer/layout.html')
    flash("Login first as a Executive","danger")
    return redirect(url_for('login'))


@app.route('/customer/home')
def home():
    if session.get('username') and session.get('type')=='executive':
            return render_template('Customer/home.html')
    flash("Login first as a Executive","danger")
    return redirect(url_for('login'))


@app.route('/customer/create',methods=['GET','POST'])
def create_customer():
    if session.get('username') and session.get('type')=='executive':
        with open('static/state_city.json') as datafile:
            data=json.load(datafile)
        if request.method=='POST':
            ssnid=request.form['ssnid']
            name=request.form['name']
            age=request.form['age']
            address1=request.form['address1']
            address2=request.form['address2']
            skey=int(request.form['state'])
            ckey=int(request.form['city'])
            state=data['states'][skey]['state']
            city=data['states'][skey]['city'][ckey]
            if ssnid and name and age and address1 and state and city:
                customer=models.Customer.query.filter_by(ssnid=ssnid).first()
                if(customer==None):
                    customer=models.Customer(ssnid=ssnid,name=name,age=age,
                    address_1=address1,address_2=address2,state=state,city=city
                    )
                    db.session.add(customer)
                    db.session.commit()
                    flash("Customer Created successfully!","success")
                else:
                    flash("Customer with SSN ID : "+ssnid+" already exists!","warning")
                return render_template('Customer/create_customer.html',data=data)  
        elif request.method=='GET':
             return render_template('Customer/create_customer.html',data=data)
    else:
        flash("Login first as a Executive","danger")
        return redirect(url_for('login'))

@app.route('/customer/search',methods=['GET','POST'])
def searchcustomer():
    if session.get('username') and session.get('type')=='executive':
        if request.method=='POST':
            ssnid=request.form['ssnid']
            cid=request.form['cid']
            customer=None
            if(ssnid!='' and cid==''):
                customer=models.Customer.query.filter_by(ssnid=ssnid).first()
            elif(cid!='' and ssnid==''):
                customer=models.Customer.query.filter_by(ssnid=ssnid).first()
            if customer!=None:
                print("customer data : ",customer)
                return render_template("Customer/showcustomer.html",data=customer)
            flash("Enter Valid Customer ID or SSNID","warning")
            return render_template('Customer/search.html') 
        else:
            return render_template('Customer/search.html')
    else: 
        flash("Login first as a Account Executive","danger")
    return redirect(url_for('login'))

#==========Cashier=========================
@app.route('/cashier')
def cashierIndex():
    if session.get('username') and session.get('type')=='cashier':
            return render_template('Cashier/layout.html')
    flash("Login first as a Cashier","danger")
    return redirect(url_for('login'))

    
if __name__ == '__main__':
    app.run(debug=True)