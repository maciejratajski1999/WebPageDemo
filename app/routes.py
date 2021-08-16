from flask import render_template, flash, redirect, url_for, send_from_directory
from app.forms import RegistrationForm, LoginForm, PictureForm, ProductForm
from app.utils import *
from flask_login import login_user, logout_user, current_user


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
    products = [[product.id, product.name, product.thumbnail] for product in products]
    products = split_into_groups_of_n(objects=products, n=3)
    return render_template('gallery.html', subpages=subpages, current=current, products=products)


@app.route("/products", methods=['GET'])
def products():
    current = 'products'
    products = Product.query.all()
    products = [[product.id, product.name, product.thumbnail] for product in products]
    products = split_into_groups_of_n(objects=products, n=3)
    return render_template('products.html', subpages=subpages, current=current, products=products)


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


@app.route("/manage", methods=['GET', 'POST'])
def manage():
    if current_user.is_authenticated:
        form = ProductForm()
        products = Product.query.all()
        pictures = [product.thumbnail for product in products]
        if form.validate_on_submit():
            if form.thumbnail.data:
                add_product(form)
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
        register_user(form)
        flash(f"Registered: {form.username.data}", 'alert')
        return redirect(url_for('home'))
    return render_template('register.html', subpages=subpages, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'tux.png', mimetype='image/vnd.microsoft.icon')
