from flask import render_template, flash, redirect, url_for
from app.forms import RegistrationForm, LoginForm, PictureForm, ProductForm
from app import app, db, bcrypt
from app.models import User, Product, Picture
from flask_login import login_user, logout_user, current_user
import os
from PIL import Image
from werkzeug.utils import secure_filename

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

@app.route("/gallery", methods=['GET', 'POST'])
def gallery():
    current = 'gallery'
    products = Product.query.all()
    pictures = [product.thumbnail for product in products]
    return render_template('gallery.html', subpages=subpages, current=current, pictures=pictures)


@app.route("/product", methods=['GET', 'POST'])
def product():
    product_id = 1
    product = Product.query.get(product_id)
    if product:
        pictures = [picture.path for picture in product.pictures]
        current = 'gallery'
        if current_user.is_authenticated:
            form = PictureForm()
            return render_template('gallery.html', subpages=subpages, current=current, pictures=pictures, form=form)
        else:
            return render_template('gallery.html', subpages=subpages, current=current, pictures=pictures)
    else:
        flash(f"Product {product_id} doesn't exist", 'alert')
        return redirect('home')

def save_picture(file_field_form):
    picture_path = os.path.join(app.root_path, 'static/thumbnails', file_field_form.filename)
    file_field_form.save(picture_path)
    return "thumbnails/" + file_field_form.filename
@app.route("/manage", methods=['GET', 'POST'])
def manage():
    if current_user.is_authenticated:
        form = ProductForm()
        products = Product.query.all()
        pictures = [product.thumbnail for product in products]
        if form.validate_on_submit():
            if form.thumbnail.data:
                thumbnail_path = save_picture(form.thumbnail.data)
                new_product = Product(name=form.name.data, thumbnail=thumbnail_path)
                db.session.add(new_product)
                db.session.commit()
                return redirect('manage')
        return render_template('manage.html', subpages=subpages, pictures=pictures, form=form)
    return render_template('home.html', subpages=subpages)

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