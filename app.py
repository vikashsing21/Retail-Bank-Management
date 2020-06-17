from flask import Flask, jsonify, render_template, request, session, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from _datetime import datetime
from form import RegistrationForm,LoginForm,CreateCustomerForm
import json



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
import models
migrate = Migrate(app, db)

# index page
#this route also checks if a user is already logged in or not
@app.route('/')
def login():
    form = LoginForm()
    if session.get('username') and session.get('type')=='executive':
            return redirect('/customer')
    elif session.get('username') and session.get('type')=='cashier':
            return redirect('/cashier') 
    else:
        return render_template('login.html',form=form)


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
    form = RegistrationForm()
    if request.method=='POST' and form.validate():
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
            else:
                flash('User with given Username already exists.','danger')
    return render_template('register.html',form=form)


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
@app.route('/customer/home')
def home():
    if session.get('username') and session.get('type')=='executive':
            return render_template('Customer/home.html')
    flash("Login first as a Executive","danger")
    return redirect(url_for('login'))


# @app.route('/customer/home')
# def home():
#     if session.get('username') and session.get('type')=='executive':
#             return render_template('Customer/home.html')
#     flash("Login first as a Executive","danger")
#     return redirect(url_for('login'))


@app.route('/customer/create',methods=['GET','POST'])
def create_customer():
    c_message="Customer Created successfully!"
    if session.get('username') and session.get('type')=='executive':
        
        with open('static/state_city.json') as datafile:
            data=json.load(datafile)
        if request.method=='POST':
            ssnid=request.form['ssnid']
            name=request.form['name']
            age=request.form['age']
            address=request.form['address']
            skey=int(request.form['state'])
            ckey=int(request.form['city'])
            state=data['states'][skey]['state']
            city=data['states'][skey]['city'][ckey]
            if ssnid and name and age and address and state and city:
                customer=models.Customer.query.filter_by(ssnid=ssnid).first()
                if(customer==None):
                    customer=models.Customer(ssnid=ssnid,name=name,age=age,
                    address=address,state=state,city=city
                    )
                    db.session.add(customer)
                    db.session.commit()
                    customer=models.Customer.query.filter_by(ssnid=ssnid).first()
                    c_status=models.CustomerStatus(customer_cid=customer.cid,customer_ssnid=customer.ssnid,message=c_message,status="active")
                    db.session.add(c_status)
                    db.session.commit()
                    flash(c_message,"success")
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
            print("Cid : {} SId {}".format(cid,ssnid))
            customer=None
            if(ssnid!='' and cid==''):
                customer=models.Customer.query.filter_by(ssnid=ssnid).first()
            elif(cid!='' and ssnid==''):
                customer=models.Customer.query.filter_by(cid=cid).first()
            if customer!=None:
                return render_template("Customer/showcustomer.html",data=customer)
            flash("Enter Valid either of Customer ID or SSNID","warning")
            return render_template('Customer/search.html') 
        else:
            return render_template('Customer/search.html')
    else: 
        flash("Login first as a Account Executive","danger")
    return redirect(url_for('login'))


@app.route('/customer/update/<id>',methods=['GET','POST'])
def update(id):
    c_message="Customer Updated Successfully!"
    if session.get('username') and session.get('type')=='executive':
        customer = models.Customer.query.filter_by(ssnid=id).first()        
        
        if request.method == 'POST':
            # return "name {0}".format(request.form['name'])
            name=request.form['name']
            age=request.form['age']
            address=request.form['address']
            if(name):
                customer.name = name
            if(age):
                customer.age  = age
            if(address):
                customer.address = address
            if name or age or address:
                db.session.commit()
                c_status = models.CustomerStatus.query.filter_by(customer_ssnid=id).first()
                c_status.message=c_message
                db.session.commit()
                flash(c_message,"success")
            else:
                 flash("No Changes were made","success")
            return redirect(url_for('searchcustomer'))

                  
        elif request.method=='GET':
            
            return render_template("Customer/update_customer.html",data=customer)
    else: 
        flash("Login first as a Account Executive","danger")
    return redirect(url_for('login'))

@app.route("/customer/delete/<id>",methods=['GET','POST'])    
def delete(id):
    c_message="Customer Deleted Successfully!"
    if session.get('username') and session.get('type')=='executive':
        customer = models.Customer.query.filter_by(ssnid=id).first()        
        if request.method=='POST':
            c_status = models.CustomerStatus.query.filter_by(customer_ssnid=id).first()
            db.session.delete(customer)
            db.session.commit()
            # c_status.customer_cid=None
            # c_status.customer_ssnid=customer.ssnid
            c_status.message=c_message
            c_status.status="inactive"
            db.session.commit()
            flash(c_message,"success")
            return redirect(url_for('searchcustomer'))
        else:
            return render_template('Customer/delete_customer.html',data=customer)         
    else: 
        flash("Login first as a Account Executive","danger")
    return redirect(url_for('login'))


@app.route("/customer/create_account/",methods=['GET','POST'])
def create_account():
    a_message="Account Created successfully!"
    if session.get('username') and session.get('type')=='executive':
        if request.method=='POST':
            cid=request.form['cid']
            customer=models.Customer.query.filter_by(cid=cid).first()
            if customer!=None:
                cid=request.form['cid']
            accnt_type=request.form['accnt_type']
            ammount=int(request.form['ammount'])
            if cid and accnt_type and ammount and customer:
                account=models.Account.query.filter_by(customer_cid=cid,accnt_type=accnt_type).first()
                if(account==None):
                    account=models.Account(customer_cid=cid,accnt_type=accnt_type,ammount=ammount
                    )
                    db.session.add(account)
                    db.session.commit()
                    account=models.Account.query.filter_by(customer_cid=cid,accnt_type=accnt_type).first()
                    a_status=models.AccountStatus(account_id=account.accntid,customer_cid=account.customer_cid,accnt_type=account.accnt_type,message=a_message,status="active")
                    db.session.add(a_status)
                    db.session.commit()
                    flash(a_message,"success")
                else:
                    flash("Account of Customer with CID : "+cid+" and Type : "+accnt_type+" already exists!","warning")
            else:
                flash("Customer with CID : "+cid+" doesn't exists!","warning")
        return render_template('Customer/create_account.html')           
    else:
        flash("Login first as a Executive","danger")
        return redirect(url_for('login'))


@app.route("/customer/account_search/",methods=['GET','POST'])
def acc_search():
    if session.get('username') and session.get('type')=='executive':
        if request.method=='POST':
            customer_cid=request.form['cid']
            accntid=request.form['accntid']
            account=None
            # using customer id multiple accounts are possible
            if(customer_cid!='' and accntid==''):
                account=models.Account.query.filter_by(customer_cid=customer_cid).all()

            # using account id only one account is possible
            elif(accntid!='' and customer_cid==''):
                account=models.Account.query.filter_by(accntid=accntid).all()

            if account:
                return render_template("Customer/showaccount.html",data=account)
            flash("Enter Valid either of Customer ID or Account Id","warning")
            return render_template('Customer/account_search.html') 
        else:
            return render_template('Customer/account_search.html')
    else: 
        flash("Login first as a Account Executive","danger")
    return redirect(url_for('login'))

# Customer status
@app.route("/customer/customer_status")
def cus_status():
    if session.get('username') and session.get('type')=='executive':
        c_status=models.CustomerStatus.query.all()
        if c_status:
            return render_template("Customer/customer_status.html",data=c_status)
        else:
            flash("No Customre Status Records available, Create an Account first!")
            return redirect(url_for('create_customer'))
    else: 
        flash("Login first as a Account Executive","danger")
    return redirect(url_for('login'))

# Account status
@app.route("/customer/account_status")
def acc_status():
    if session.get('username') and session.get('type')=='executive':
        a_status=models.AccountStatus.query.all()
        if a_status:
            return render_template("Customer/customer_status.html",data=a_status)
        else:
            flash("No Account Status records available, Create an account first!")
            return redirect(url_for('create_account'))
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

