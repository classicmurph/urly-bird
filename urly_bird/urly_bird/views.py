from .app import app
from flask import render_template, flash, redirect, request, url_for
from . import models
from .models import User
from .utils import flash_errors
from .forms import RegistrationForm, LoginForm
from flask.ext.login import login_user, login_required, logout_user, LoginManager

"""Add your views here."""


login_manager = LoginManager()
@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect("login.html")


@app.route("/")
def index():
    # books = Book.query.all()
    return render_template("layout.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get("next") or url_for("index"))
        else:
            flash("That email or password is not correct.")

    flash_errors(form)
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("A user with that email address already exists.")
        else:
            user = User(name=form.name.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("You have been registered and logged in.")
            return redirect(url_for("index"))
    else:
        flash_errors(form)

    return render_template("register.html", form=form)