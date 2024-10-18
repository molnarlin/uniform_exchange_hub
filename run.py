import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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

@app.route("/")
def index():
    return render_template('index.html')

def get_user_data(form):
    return {
        "user_name": form.get("user_name").lower(),
        "contact_email": form.get("contact_email").lower(),
        "contact_person": form.get("contact_person"),
        "contact_phone": form.get("contact_phone"),
        "contact_address": form.get("contact_address"),
        "school_name": form.get("school_name"),
        "event_place": form.get("event_place"),
        "event_date": form.get("event_date"),
        "items": form.getlist("items")
    }

@app.route("/users")
def get_users():
    users = mongo.db.users.find()
    return render_template("users.html", users=users)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_query = request.form.get("search_query")
        results = mongo.db.users.find({"$or": [{"school_name": {"$regex": search_query, "$options": "i"}}, {"items": {"$regex": search_query, "$options": "i"}}]})
        return render_template("search_result.html", results=results, search_query=search_query)
    return render_template("search.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("user_name").lower()
        
        if mongo.db.users.find_one({"user_name": username}):
            flash("Username already exists")
            return redirect(url_for("register"))
        mongo.db.users.insert_one({
            "user_name": username,
            "user_password": generate_password_hash(request.form.get("user_password"))
        })

        session["user"] = username
        flash("Registration Successful!")
        return redirect(url_for("user_profile", user_name=session["user"]))
    return render_template("register.html")
        

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.permanent  = True
        username = request.form.get("user_name").lower()
        user = mongo.db.users.find_one({"user_name": username})
    
        if user and check_password_hash(user["user_password"], request.form.get("user_password")):
            session["user"] = username
            flash(f"Welcome, {username}")
            return redirect(url_for("user_profile", user_name=session["user"]))
        
        flash("Incorrect Username and/or Password")
        return redirect(url_for("login"))

    return render_template("login.html")

    
@app.route("/user_profile/<user_name>")
def user_profile(user_name):
    user = mongo.db.users.find_one({"user_name": user_name})
    if user is None:
            flash("User  not found")
            return redirect(url_for("index"))
    return render_template("user_profile.html", user=user)
               

@app.route("/edit_user/<user_name>", methods=["GET", "POST"])
def edit_user(user_name):

    # Retrieve the user from the database
    user_to_edit = mongo.db.users.find_one({"user_name": user_name})

    if user_to_edit is None:
        flash("User  not found")
        return redirect(url_for("index"))
   
    if request.method == "POST":
        mongo.db.users.update_one({"user_name": user_name}, {
            "$set": get_user_data(request.form)
        })
        flash("User  Successfully Updated")

    return render_template("edit_user.html", user=user_to_edit)


@app.route("/delete_user/<user_name>")
def delete_user(user_name):
    mongo.db.users.delete_one({"user_name": user_name})
    flash("User Successfully Deleted")
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    # remove user from session cookie
    session.pop("user", None)
    flash("You have been logged out!", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)