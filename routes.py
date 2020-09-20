from app import app
from flask import render_template, request, redirect, abort
import users, feeds
from os import path
from werkzeug.utils import secure_filename
from slugify import slugify

import calendar;
import time;


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/feed', methods=["get","post"])
def create_feed():
    if request.method == "GET":
        return render_template("new_feed.html")
    if request.method == "POST":
        secret = slugify(request.form["secret"])
        if len(secret) > 50:
            return render_template("new_feed.html", error="Secret should be under 200 characters.")
        title = request.form["title"]
        if len(title) > 199:
            return render_template("new_feed.html", error="Title should be under 200 characters.")
        description = request.form["description"]
        if len(description) > 199:
            return render_template("new_feed.html", error="Description should be under 200 characters.")
        if feeds.create_feed(secret, title, description):
            return redirect("/feed/"+secret)
        else:
            return render_template("new_feed.html",error="Could not create feed. Try with different secret.")

@app.route('/feed/<string:secret>/<int:id>', methods=["post", "delete"])
def modify_item(secret, id):
    if request.method == "POST":
        if request.form["action"] == 'delete' and feeds.delete_item(secret, id):
            return redirect("/feed/"+secret)
        else:
            abort(400)
    else:
        return redirect("/feed/"+secret)

@app.route('/feed/<string:secret>/new')
def create_item(secret):
    return render_template("new_item.html", secret=secret)

@app.route('/feed/<string:secret>', methods=["get","post"])
def feed(secret):
    if request.method == "GET":
        feed = feeds.get_feed(secret)
        if feed == None and users.user_id() == 0:
            return redirect("/login")
        elif feed == None:
            return redirect("/feed")
        else:
            items = feeds.get_items(secret)
            return render_template("feed.html", feed=feed, items=items, secret=secret)
    if request.method == "POST":
        if request.form.get("action", False) == "delete":
            if feeds.delete_feed(secret):
                return redirect("/")
            return render_template("feed.html",error="Does not work :(")
        elif request.files['image']:
            feed = feeds.get_feed(secret)
            if feed == None or feed == 0 or users.user_id() == 0:
                abort(400)
            description = request.form["description"]
            if len(description) > 199:
                return render_template("feed.html", error="Description should be under 200 characters.")
            uploaded_file = request.files['image']
            filename = uploaded_file.filename
            if filename == '':
                abort(400)
            file_ext = path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            file_path = path.join('static/uploads', secure_filename(secret + '-' + str(calendar.timegm(time.gmtime())) + '-' +filename))
            uploaded_file.save(file_path)
            if feeds.create_item(secret, file_path, description):
                return redirect("/feed/"+secret)
            else:
                return render_template("feed.html",error="Does not work :(")
        else:
            return render_template("feed.html",error="Does not work :(")

@app.route("/login", methods=["get","post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("login.html",error="Wrong username / password")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/signup", methods=["get","post"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) > 50 or len(password) > 50:
            return render_template("signup.html",error="Username & password should be under 50 characters.")
        if len(username) < 4 or len(password) < 4:
            return render_template("signup.html",error="Username & password should be over 3 characters.")
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("signup.html",error="Failed create account.")