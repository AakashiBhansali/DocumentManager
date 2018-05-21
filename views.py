from app import app
from flask import request, jsonify, render_template, url_for, flash, session, redirect
from models import createUser,checkUser, addDocument, getDocuments, delDocument
from extra import *
from bson.objectid import ObjectId
import datetime
from functools import wraps

def check_session(login_needed):
    def decorated_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if login_needed :
                if 'email' in session:
                    return func(*args, **kwargs)
                else:
                    return redirect(url_for('login'))
            else:
                if 'email' in session:
                    return redirect(url_for('manage_document'))
                else:
                    return func(*args, **kwargs)
        return wrapper
    return decorated_function

@app.route('/')
@check_session(True)
def home():
    return redirect(url_for('manage_document'))

@app.route('/login',methods=['GET','POST'])
@check_session(False)
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = {}
        data["email"] = request.form["InputEmail"]
        result = checkUser(data)
        if (result["success"]):
            if (result["exists"]):
                hashed_password = result["user"]["password"]
                if(check_password(hashed_password, request.form["InputPassword"])):
                    session['name'] = result["user"]["firstName"] + ' ' + result["user"]["lastName"]
                    session['email'] = result["user"]["email"]
                    return redirect(url_for('manage_document'))
            flash('Invalid Login Credentials', {'header' : 'Sorry!!', 'class' : 'alert-danger'})
            return redirect(url_for('login'))
        else:
            flash('Some error occured. Please try again!',{'header' : 'Oops!!', 'class' : 'alert-danger'})
            return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
@check_session(False)
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        error = checkRegistrationForm(request.form)
        if error:
            return render_template('register.html',error=error)
        else:
            data = {}
            data['email'] = request.form['InputEmail']
            result = checkUser(data)
            if result['success']:
                if result['exists']:
                    flash('User already registered.', {'header' : 'Oops!!', 'class' : 'alert-danger'})
                    return redirect(url_for('register'))
                else:
                    data['firstName'] =  request.form['InputFirstName']
                    data['lastName'] =  request.form['InputLastName']
                    data['password'] =  hash_password(request.form['InputPassword'])
                    result = createUser(data)
                    if result['success']:
                        flash ('User registered',{'header' : 'Success!!', 'class' : 'alert-success'})
                        return redirect(url_for('login'))
                    else:
                        flash ('Some error occured. Please try again!',{'header' : 'Oops!!', 'class' : 'alert-danger'})
                        return redirect(url_for('register'))
            else:
                flash ('Some error occured. Please try again!',{'header' : 'Oops!!', 'class' : 'alert-danger'})
                return redirect(url_for('register'))

@app.route('/add-document',methods=['GET','POST'])
@check_session(True)
def add_document():
    fullDate = datetime.datetime.now().strftime("%Y-%m-%d")
    monthDate = datetime.datetime.now().strftime("%Y-%m")
    if request.method == 'GET':
        return render_template('add_document.html',fullDate = fullDate, monthDate=monthDate)
    elif request.method == 'POST':
        error = checkDocumentForm(request.form)
        if error:
            return render_template('add_document.html',fullDate = fullDate, monthDate=monthDate,error=error)
        else:
            form = request.form
            data = {}
            data['email'] = session['email']
            data['DocType'] = form['DocType']
            if (data['DocType'] == 'Driving Licence'):
                data['DLNumber'] = form['DLNumber']
                data['DLValidity'] = form['DLValidity']
                data['DLDOB'] = form['DLDOB']
                data['DLName'] = form['DLName']
                data['DLMiddleName'] = form['DLMiddleName']
                data['DLAddress'] = form['DLAddress']
            elif (data['DocType'] == 'Aadhar Card'):
                print('Aadhar Card')
                data['AANumber'] = form['AANumber']
                data['AADOB'] = form['AADOB']
                data['AAName'] = form['AAName']
                data['AAAddress'] = form['AAAddress']
            elif (data['DocType'] == 'Debit Card'):
                data['DCNumber'] = form['DCNumber']
                data['DCName'] = form['DCName']
                data['DCValidity'] = form['DCValidity']
                data['DCCVV'] = form['DCCVV']
            result = addDocument(data)
            if result['success']:
                flash('Document Uploaded', {'header': 'Success!!', 'class': 'alert-success'})
            else:
                flash('Some error occured. Please try again!', {'header': 'Oops!!', 'class': 'alert-danger'})
            return redirect(url_for('add_document'))

@app.route('/manage-document', methods=['GET','POST'])
@check_session(True)
def manage_document():
    if request.method == 'POST':
            id = ObjectId(request.form['delete'])
            print(delDocument({'_id': id}))
            flash('Document Deleted', {'header': 'Success!!', 'class': 'alert-success'})
    documents = getDocuments({'email':session['email']})
    print(documents.count())
    return render_template('manage_document.html',documents = documents)

@app.route('/profile')
@check_session(True)
def profile():
    return render_template('profile.html')

@app.route('/change-password')
@check_session(True)
def change_password():
    return render_template('change_password.html')

@app.route('/edit-document')
@check_session(True)
def edit_document():
    return render_template('add_document.html')

@app.route('/logout')
@check_session(True)
def logout():
    del session['email']
    del session['name']
    return redirect(url_for('login'))