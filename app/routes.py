from flask import render_template, flash, redirect, url_for
from app.forms import RegistrationForm, LoginForm
from app import app, db, bcrypt
from app.models import User
from flask_login import login_user, logout_user, current_user

subpages = {'home' : {"Home" : "/"}, 'about' : {"About" : "/about"}, 'gallery' : {"Gallery" : "/gallery"}}

@app.route("/")
@app.route("/home")
def home():
    current = 'home'
    return render_template('home.html', subpages=subpages, current=current)

@app.route("/about")
def about():
    current = 'about'
    return render_template('about.html', subpages=subpages, current=current)

images = ['tux.png' for i in range(10)]
@app.route("/gallery")
def gallery():
    current = 'gallery'
    return render_template('gallery.html', subpages=subpages, current=current, images=images)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f"Already logged in as {current_user.username}", 'alert')
        return redirect('home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful", 'alert')
    return render_template('login.html', subpages=subpages, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f"Already logged in as {current_user.username}", 'alert')
        return redirect('home')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Registered: {form.username.data}", 'alert')
        return redirect(url_for('home'))
    return render_template('register.html', subpages=subpages, form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))