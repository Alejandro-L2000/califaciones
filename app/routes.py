from app.forms import LoginForm
from app import app
from flask import render_template, redirect, url_for

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Lidera con datos del Login
        return redirect(url_for("index"))
    else:
        return render_template("login.html", form=form)