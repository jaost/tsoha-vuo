from app import app
from flask import render_template, request, redirect, abort
import users, feeds
from os import path
from werkzeug.utils import secure_filename
from slugify import slugify

import calendar
import time

import sys


@app.route("/")
def index():
    if users.user_id() != 0:
        feed_list = feeds.get_feeds()
    else:
        feed_list = []
    return render_template("index.html", feed_list=feed_list)


@app.route("/feed", methods=["get", "post"])
def create_feed():
    error = []
    if request.method == "GET":
        return render_template("new_feed.html")
    if request.method == "POST":
        secret = slugify(request.form["secret"])
        if len(secret) < 5 or len(secret) > 50:
            error.append("Secret should be more than 4 and under 200 characters.")
        title = request.form["title"]
        if len(title) < 5 or len(title) > 199:
            error.append("Title should be more than 4 and under 200 characters.")
        description = request.form["description"]
        if len(description) < 5 or len(description) > 199:
            error.append("Description should be more than 4 and under 200 characters.")
        if len(error) == 0 and feeds.create_feed(secret, title, description):
            return redirect("/feed/" + secret)
        else:
            error.append("Could not create feed. Try with different secret.")
            return render_template(
                "new_feed.html",
                secret=secret,
                title=title,
                description=description,
                error=error,
            )


@app.route("/feed/<string:secret>/<int:id>", methods=["post", "delete"])
def modify_item(secret, id):
    if request.method == "POST":
        if request.form.get("action", False) == "delete" and feeds.delete_item(
            secret, id
        ):
            return redirect("/feed/" + secret)
        if request.form.get("action", False) == "vote" and feeds.vote_item(secret, id):
            return redirect("/feed/" + secret + "#I-" + str(id))
        else:
            abort(400)
    else:
        return redirect("/feed/" + secret)


@app.route("/feed/<string:secret>/new")
def create_item(secret):
    return render_template("new_item.html", secret=secret)


@app.route("/feed/<string:secret>", methods=["get", "post"])
def feed(secret):
    feed = feeds.get_feed(secret)
    error = []
    if request.method == "GET":
        if feed == None and users.user_id() == 0:
            return redirect("/login")
        elif feed == None:
            return redirect("/feed")
        else:
            items = feeds.get_items(secret)
            votes = feeds.get_feed_votes(secret)
            return render_template("feed.html", feed=feed, items=items, votes=votes, secret=secret)
    if request.method == "POST":
        if request.form.get("action", False) == "delete":
            if feeds.delete_feed(secret):
                return redirect("/")
            return render_template(
                "feed.html", secret=secret, error=["Could not delete item."]
            )
        elif request.form.get("action", False) == "new_item":
            if not request.files["image"]:
                error.append("No image found.")
            feed = feeds.get_feed(secret)
            if feed == None or feed == 0 or users.user_id() == 0:
                error.append("Feed not found or user not logged in.")
            description = request.form["description"]
            if len(description) < 3 or len(description) > 199:
                error.append(
                    "Description should be more than 3 and under 200 characters."
                )
            uploaded_file = request.files["image"]
            filename = uploaded_file.filename
            if len(filename) < 3 or len(filename) > 30:
                error.append("Filename should be between 3 and 30 characters.")
            file_ext = path.splitext(filename)[1]
            if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
                error.append("Filetype is not supported")
            if len(error) > 0:
                return render_template(
                    "new_item.html",
                    secret=secret,
                    image=request.files["image"],
                    description=description,
                    error=error,
                )
            file_path = path.join(
                "static/uploads",
                secure_filename(
                    secret + "-" + str(calendar.timegm(time.gmtime())) + "-" + filename
                ),
            )
            uploaded_file.save(file_path)
            if feeds.create_item(secret, file_path, description):
                return redirect("/feed/" + secret)
            else:
                return render_template(
                    "new_item.html",
                    secret=secret,
                    error=["Something went wrong. Try again later."],
                )
        else:
            return render_template("feed.html", feed=feed, error=["Does not work :("])


@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template(
                "login.html", username=username, error=["Wrong username / password"]
            )


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/signup", methods=["get", "post"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        error = []
        username = request.form["username"]
        password = request.form["password"]
        if len(username) > 50 or len(password) > 50:
            error.append("Username & password should be under 50 characters.")
        if len(username) < 4 or len(password) < 4:
            error.append("Username & password should be over 3 characters.")

        if len(error) == 0 and users.register(username, password):
            return redirect("/")
        else:
            error.append("Failed create account.")
            return render_template("signup.html", username=username, error=error)