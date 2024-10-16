import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from bson.errors import *
from datetime import timedelta
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.permanent_session_lifetime = timedelta(minutes=10)

mongo = PyMongo(app)
db = mongo.db

@app.route("/")
def index():
    return render_template('index.html')

class User:
    def __init__(self, user_name, contact_email, contact_person, contact_phone, contact_address, school_name, event_place, event_date, items):
        self.user_name = user_name
        self.contact_email = contact_email
        self.contact_person = contact_person
        self.contact_phone = contact_phone
        self.contact_address = contact_address
        self.school_name = school_name
        self.event_place = event_place
        self.event_date = event_date
        self.items = items

    def save(self):
        user_data = {
            "user_name": self.user_name,
            "contact_email": self.contact_email,
            "contact_person": self.contact_person,
            "contact_phone": self.contact_phone,
            "contact_address": self.contact_address,
            "school_name": self.school_name,
            "event_place": self.event_place,
            "event_date": self.event_date,
            "items": self.items
        }
        db.users.insert_one(user_data)


@app.route("/users")
def get_users():
    users = mongo.db.users.find()
    return render_template("users.html", users=users)


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    search_results = db.users.aggregate([
        {
            '$search': {
                'index': 'users_information',
                'text': {
                    'query': query,
                    'path': 'users_information'
                }
            }
        }
    ])
    return render_template('users.html', users=search_results)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user_username = mongo.db.users.find_one(
            {"user_name": request.form.get("user_name").lower()})
        existing_user_email = mongo.db.users.find_one({"contact_email": request.form.get("contact_email").lower()})
        if existing_user_username or existing_user_email:
            flash("Username or email address already exists")
            return redirect(url_for("register"))

        register = {
            "user_name": request.form.get("user_name").lower(),
            "user_password": generate_password_hash(request.form.get("user_password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("user_name").lower()
        flash("Registration Successful!")
        return redirect(url_for("user_profile", user_name=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent  = True
    
        # check if username exists in db
        existing_user = mongo.db.users.find_one({"user_name": request.form.get("user_name").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(existing_user["user_password"], request.form.get("user_password")):
                session["user"] = request.form.get("user_name").lower()
                flash("Welcome, {}".format(request.form.get("user_name")))
                
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/create_profile/<user_name>")
def create_profile(user_name):
    user = mongo.db.users.find_one({"user_name": user_name})
    if "user":
    # grab the session user's username from db
        return render_template("create_profile.html", user=user)

    else:
        flash("User not found")
        return redirect(url_for("index"))
    
@app.route("/user_profile", methods=["GET", "POST"])
def user_profile():
    user_name = session["user"]
    user = mongo.db.users.find_one({"user_name": user_name})
    if user:
        if request.method == "POST":
            contact_email = request.form.get["contact_email"]
            contact_person = request.form.get["contact_person"]
            contact_phone = request.form.get["contact_phone"]
            contact_address = request.form.get["contact_address"]
            school_name = request.form.get["school_name"]
            event_place = request.form.get["event_place"]
            event_date = request.form.get["event_date"]
            items = request.form.get["items"]
            session["user_name"] = user_name
            mongo.db.users.update_one({"user_name": user_name}, {
                "$set": {
                    "contact_email": contact_email,
                    "contact_person": contact_person,
                    "contact_phone": contact_phone,
                    "contact_address": contact_address,
                    "school_name": school_name,
                    "event_place": event_place,
                    "event_date": event_date,
                    "items": items
                }
            })
            flash("Data was saved!")
        else:
            if "user_name" in session:
                user_name = session["user_name"]
        return render_template("user_profile.html", user=user)
    else:
        flash("User not found")
        return redirect(url_for("login"))


@app.route("/edit_user/<user_name>", methods=["GET", "POST"])
def edit_user(user_name):

    # Retrieve the user from the database
    user_to_edit = mongo.db.users.find_one({"user_name": user_name})

    if user_to_edit is None:
        flash("User  not found")
        return redirect(url_for("index"))
   
    if request.method == "POST":
        submit = {
            "$set": {
                "school_name": request.form.get("school_name"),
                "user_name": request.form.get("user_name"),
                "contact_person": request.form.get("contact_person"),
                "contact_phone": request.form.get("contact_phone"),
                "contact_email": request.form.get("contact_email"),
                "contact_address": request.form.get("contact_address"),
                "event_date": request.form.get("event_date"),
                "event_place": request.form.get("event_place"),
                "items": request.form.getlist("items"),
                "created_by": session.get["user"]
            }
        }
        mongo.db.users.update_one({"user_name": user_name}, submit)
        flash("User Successfully Updated")

    return render_template("edit_user.html", user=user_to_edit)


@app.route("/delete_user/<user_name>")
def delete_user(user_name):
    mongo.db.users.delete_one({"user_name": user_name})
    flash("User Successfully Deleted")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    # remove user from session cookie
    if "user" in session:
        user = session["user"]
        flash("You have been logged out!", "info")
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)