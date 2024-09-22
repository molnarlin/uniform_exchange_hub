import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_users")
def get_users():
    users = list(mongo.db.users.find())
    return render_template("index.html", users=users)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    users = list(mongo.db.users.find({"$text": {"$search": query}}))
    return render_template("users.html", users=users)


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
        return redirect(url_for("profile", user_name=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"user_name": request.form.get("user_name").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["user_password"], request.form.get("user_password")):
                        session["user"] = request.form.get("user_name").lower()
                        flash("Welcome, {}".format(
                            request.form.get("user_name")))
                        return redirect(url_for(
                            "profile", user_name=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<user_name>", methods=["GET", "POST"])
def profile(user_name):
    # grab the session user's username from db
    user_name = mongo.db.users.find_one(
        {"user_name": session["user"]})["user_name"]

    if session["user"]:
        return render_template("profile.html", user_name=user_name)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
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
            "created_by": session["user"]
        }
        mongo.db.users.update({"_id": ObjectId(user_id)}, submit)
        flash("User Successfully Updated")

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    schools = mongo.db.schools.find().sort("school_name", 1)
    return render_template("edit_user.html", user=user, schools=schools)


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    flash("User Successfully Deleted")
    return redirect(url_for("index"))


@app.route("/get_schools")
def get_schools():
    schools = list(mongo.db.schools.find().sort("school_name", 1))
    return render_template("schools.html", schools=schools)


@app.route("/add_school", methods=["GET", "POST"])
def add_school():
    if request.method == "POST":
        school = {
            "school_name": request.form.get("school_name")
        }
        mongo.db.schools.insert_one(school)
        flash("New School Added")
        return redirect(url_for("get_schools"))

    return render_template("index.html")


@app.route("/edit_school/<school_id>", methods=["GET", "POST"])
def edit_school(school_id):
    if request.method == "POST":
        submit = {
            "school_name": request.form.get("school_name")
        }
        mongo.db.schools.update({"_id": ObjectId(school_id)}, submit)
        flash("School Successfully Updated")
        return redirect(url_for("get_schools"))

    school = mongo.db.schools.find_one({"_id": ObjectId(school_id)})
    return render_template("edit_schools.html", school=school)


@app.route("/delete_school/<school_id>")
def delete_school(school_id):
    mongo.db.schools.remove({"_id": ObjectId(school_id)})
    flash("School Successfully Deleted")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP", "0.0.0.0"),
        port=int(os.environ.get("PORT", "5000")),
        debug=True)