import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user
if os.path.exists("env.py"):
    import env

app = Flask(__name__)
client = MongoClient("MONGO_URI")
db = client.uniform_hub

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.get('_id')
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.school_name = user_data.get('school_name')
        self.contact_person = user_data.get('contact_person')
        self.contact_phone = user_data.get('contact_phone')
        self.contact_address = user_data.get('contact_address')
        self.event_date = user_data.get('event_date')
        self.event_place = user_data.get('event_place')
        self.items = user_data.get('items')

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': user_id})
    if user_data:
        return User(user_data)
    return None

@app.route("/")
def index():
    users = list(mongo.db.users.find())
    return render_template('index.html', users=users)


@app.route("/users")
@login_required
def get_users():
    return render_template("users.html", user=current_user)


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
        existing_user = mongo.db.users.find_one(
            {"user_name": request.form.get("user_name").lower()})

        if existing_user:
            flash("Username already exists")
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
        user_name = request.form.get("user_name").lower()
        user_password = request.form.get("user_password")
        # check if username exists in db
        existing_user = mongo.db.users.find_one({"user_name": user_name})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(existing_user["user_password"], user_password):
                session["user"] = user_name
                flash("Welcome, {}".format(user_name))
                return redirect(url_for("user_profile", user_name=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
    
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/create_profile/<user_name>")
@login_required
def create_profile(user_name):
    user = mongo.db.users.find_one({"user_name": user_name})
    if "user":
    # grab the session user's username from db
        return render_template("create_profile.html", user=user)

    else:
        flash("User not found")
        return redirect(url_for("index"))
    
@app.route("/user_profile/<user_name>")
@login_required
def user_profile(user_name):
    user = mongo.db.users.find_one({"user_name": user_name})
    if user:
        return render_template("user_profile.html", user=user)
    else:
        flash("User not found")
        return redirect(url_for("index"))


@app.route("/edit_user/<user_name>", methods=["GET", "POST"])
def edit_user(user_name):
    if request.method == "POST":
        submit = {
            "school_name": request.form.get("school_name"),
            "user_name": request.form.get("user_name"),
            "contact_person": request.form.get("contact_person"),
            "contact_phone": request.form.get("contact_phone"),
            "contact_email": request.form.get("contact_email"),
            "contact_address": request.form.get("contact_address"),
            "event_date": request.form.get("event_date"),
            "event_place": request.form.get("event_place"),
            "items": request.form.get("items"),
            "created_by": session.get["user"]
        }
        mongo.db.users.update_one({"user_name": user_name}, {"$set": submit})
        flash("User Successfully Updated")
        return redirect(url_for("get_users"))

    user = mongo.db.users.find_one({"user_name": user_name})
    return render_template("edit_user.html", user=user)


@app.route("/delete_user/<user_id>")
def delete_user(user_name):
    mongo.db.users.remove({"user_name": user_name})
    flash("User Successfully Deleted")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)