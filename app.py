from functools import wraps
from flask import Flask
from flask import redirect, url_for, render_template
import pyrebase
from flask import request,session
from flask import flash


config = {
    "apiKey": "AIzaSyAO50b9Y1qkVB79BTW29SqKaiIt0VkS238",
    "authDomain": "pgms-65b22.firebaseapp.com",
    "projectId": "pgms-65b22",
    "storageBucket": "pgms-65b22.appspot.com",
    "messagingSenderId": "116368140879",
    "appId": "1:116368140879:web:01b36af108a7929615983a",
    "measurementId": "G-WE0TDV70FE",
    "databaseURL": ""
  }

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__)
app.secret_key = "super secret key"

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'email' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first!!", category="danger")
            return redirect(url_for('login'))
    return wrap

@app.route("/")
@app.route("/home")
@login_required
def home():
    return "Hello World!"

    
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method =='POST':
        email = request.form['email']  
        password = request.form['pass']
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['email'] = email
            flash("Login Successfull!!", 'success')
            return redirect(url_for('home'))
        except:
            flash("Login Unsuccessfull!!", 'danger')
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been successfully logged out!!", category="success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
