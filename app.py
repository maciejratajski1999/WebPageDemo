from flask import Flask, render_template, request
from forms import RegistrationForm, LoginForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'eluwina'

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
    return render_template('login.html', subpages=subpages)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', subpages=subpages, form=form)
