from flask import render_template, flash, redirect, url_for, send_from_directory, request
from app.forms import *
from app.utils import *
from flask_login import login_user, logout_user, current_user
from time import strftime


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
    product = Product.query.get(product_id)
    if product:
        pictures = product.pictures
        pictures = [[picture.path, picture.title, delete_picture_form(picture.path)] for picture in pictures]
        pictures_split = split_into_groups_of_n(pictures, n=3)
        delete_picture_forms = [picture[2] for picture in pictures]
        for form in delete_picture_forms:
            if form.validate_on_submit():
                if form.picture_path.data:
                    pic_to_delete = get_picture(form.picture_path.data)
                    title = pic_to_delete.title
                    delete_picture(pic_to_delete)
                    flash(f'Deleted a picture: {title}', 'alert')
                    return redirect(url_for('product', product_id=product_id))
        return render_template('product.html', subpages=subpages, current=current, pictures=pictures_split)
    else:
        return redirect('products')


@app.route("/manage", methods=['GET', 'POST'])
def manage():
    if current_user.is_authenticated:
        product_form = ProductForm()
        products = Product.query.all()
        products = [product for product in products]
        picture_forms = {product.id : picture_form_id(product_id=product.id) for product in products}

        if product_form.submitproduct.data and product_form.validate_on_submit():
            if product_form.thumbnail.data:
                add_product(product_form)
                return redirect('manage')

        for picture_form in picture_forms.values():
            if picture_form.submitpicture.data and  picture_form.validate_on_submit():
                if picture_form.picture.data:
                    add_picture(picture_form)
                    return redirect(url_for('manage'))

        delete_product_forms = {product.id : delete_product_id(product.id) for product in products}
        for delete_form in delete_product_forms.values():
            if delete_form.delete.data and delete_form.validate_on_submit():
                delete_product_by_id(delete_form.product_id.data)
                return redirect(url_for('manage'))

        return render_template('manage.html', subpages=subpages, products=products, product_form=product_form, picture_forms=picture_forms, delete_forms=delete_product_forms)
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
                               'tux.png',
                               mimetype='image/vnd.microsoft.icon')

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    posts = [post for post in Post.query.all()]
    posts.reverse()
    if current_user.is_authenticated:
        form = new_blog_post(current_user.username)
        if form.submit.data and form.validate_on_submit():
            add_post(form)
            return redirect(url_for('blog'))

        delete_blog_post_forms = {post.id : delete_blog_post_form_id(post.id) for post in posts}
        for delete_form in delete_blog_post_forms.values():
            if delete_form.delete_post.data and delete_form.validate_on_submit():
                post = Post.query.get(delete_form.post_id.data)
                delete_post(post)
                return redirect(url_for('blog'))

        edit_blog_post_forms = {post.id: edit_blog_post_form_id(post.id) for post in posts}
        for edit_form in edit_blog_post_forms.values():
            if edit_form.edit.data and edit_form.validate_on_submit():
                return redirect(url_for('editpost', post_id=edit_form.post_id.data))

        return render_template('blog.html', subpages=subpages, current='blog', form=form, posts=posts,
                               delete_blog_post_forms=delete_blog_post_forms,
                               edit_blog_post_forms=edit_blog_post_forms)
    return render_template('blog.html', subpages=subpages, current='blog', posts=posts)


@app.route('/editpost', methods=['GET', 'POST'])
def editpost():
    if current_user.is_authenticated:
        post_id = int(request.args.get('post_id'))
        post = Post.query.get(post_id)
        form = edit_blog_post(post)
        if form.validate_on_submit():
            edit_post(post, form)
            return redirect('blog')
        return render_template('editpost.html', subpages=subpages, form=form)
    else:
        return redirect(url_for('home'))