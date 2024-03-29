from functools import wraps
from flask import Flask
from flask import redirect, url_for, render_template
import pyrebase
from flask import request,session
import firebase_admin
from firebase_admin import credentials
from flask import flash
from controller.complaints import fetch_complaints, fetch_single_complaint
from controller.supervisor import get_supervisors, upload_image_and_data
from controller.stats import get_complaints
from controller.complaints import fetch_complaints, closeComplaint, valid_invalid
from controller.wards import get_wards


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "pgms-65b22.appspot.com"
})

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
    complaints = get_complaints()
    return render_template('home.html.jinja', complaints=complaints)

@app.route("/complaints/<complaintType>", methods=['GET', 'POST'])
@login_required
def complaintsFunction(complaintType):
    if request.method == 'POST':
        closeComplaint(request.form['compid'])
        flash("Complaint Closed Successfully!", 'success')
        return redirect(url_for('complaintsFunction',complaintType='Resolved'))
    comps = fetch_complaints(complaintType)
    return render_template("complaints_table.html", comps=comps)

@app.route("/detailed-complaint/<complaintid>", methods=['GET','POST'])
@login_required
def detailedComplaint(complaintid):
    if request.method == 'POST':
        value = request.form['validate']
        cid = request.form['compid']
        supemail = request.form['supemail']
        closeComplaint(cid)
        valid_invalid(value, cid, supemail)
        flash("Complaint has been marked "+value+" successfully!", 'success')
        return redirect(url_for('complaintsFunction',complaintType='Closed'))

    comp = fetch_single_complaint(complaintid)
    return render_template("detailed_complaint.html", comp=comp)

@app.route("/supervisor", methods=['GET'])
@login_required
def supervisor():
    sups = get_supervisors()
    return render_template('supervisor.html',sups = sups)

@app.route("/wards", methods=['GET'])
@login_required
def wards():
    wards = get_wards()
    return render_template('ward.html',wards = wards)

@app.route("/addsupervisor", methods=['GET','POST'])
@login_required
def addsupervisor():
    profile = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        ward = request.form['ward']
        phoneno = request.form['phoneno']
        if 'profile' in request.files:
            profile = request.files['profile']
        dob = request.form['dob']
        upload_image_and_data(profile, name, email, ward, phoneno, dob)
        flash("Supervisor Added Successfully!!", 'success')
        return redirect(url_for('supervisor'))
    return render_template('add-supervisor.html')
    

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
    if 'email' in session:
        flash('Already Logged In!', 'info')
        return redirect(url_for('home'))
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been successfully logged out!!", category="success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
