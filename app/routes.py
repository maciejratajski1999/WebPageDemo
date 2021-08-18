from flask import render_template, flash, redirect, url_for, send_from_directory, request
from app.forms import *
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
    products = get_products_in_group_of_n(3)
    return render_template('products.html', subpages=subpages, current=current, products=products)


@app.route("/product", methods=['GET', 'POST'])
def product():
    current = "products"
    product_id = int(request.args.get('product_id'))
    pictures = Product.query.get(product_id).pictures
    pictures = [[picture.path] for picture in pictures]
    pictures = split_into_groups_of_n(pictures, n=3)
    return render_template('product.html', subpages=subpages, current=current, pictures=pictures)


@app.route("/manage", methods=['GET', 'POST'])
def manage():
    if current_user.is_authenticated:
        product_form = ProductForm()
        products = Product.query.all()
        products = [product for product in products]
        picture_forms = {product.id : picture_form_id(product_id=product.id) for product in products}
        if product_form.validate_on_submit():
            if product_form.thumbnail.data:
                add_product(product_form)
                return redirect('manage')
        for picture_form in picture_forms.values():
            if picture_form.validate_on_submit():
                add_picture(picture_form)
                return redirect(url_for('manage'))
        apply_changes_form = ApplyChangesForm()
        if apply_changes_form.validate_on_submit():
            if verify_password(current_user, apply_changes_form.password.data):
                new_images_count = len(save_images())
                flash(f"success, {new_images_count} new images saved in database", 'alert')
            else:
                flash(f"Wrong password for {current_user.username}", 'alert')

        return render_template('manage.html', subpages=subpages, products=products, product_form=product_form, picture_forms=picture_forms, apply_changes_form=apply_changes_form)
    return render_template('home.html', subpages=subpages)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f"Already logged in as {current_user.username}", 'alert')
        return redirect('home')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful", 'alert')
    return render_template('login.html', subpages=subpages, form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'tux.png', mimetype='image/vnd.microsoft.icon')
