from flask import render_template, flash, redirect, url_for
from app.forms import RegistrationForm, LoginForm
from app import app, db

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

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', subpages=subpages, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        from app.models import User
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Registered: {form.username.data}", 'alert')
        return redirect(url_for('home'))
    return render_template('register.html', subpages=subpages, form=form)

