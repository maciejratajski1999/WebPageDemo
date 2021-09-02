from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


class CheckboxCheck:
    def __init__(self, message=None):
        if not message:
            message = "Checkbox must be confirmed"
        self.message = message

    def __call__(self, form, field):
        if not field.data:
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, field):
        username_taken = User.query.filter_by(username=field.data).first()
        if username_taken:
            raise ValidationError("username already taken")

    def validate_email(self, field):
        email_taken = User.query.filter_by(email=field.data).first()
        if email_taken:
            raise ValidationError("email already taken")


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PictureForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()], default=0)
    picture = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png']), DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submitpicture = SubmitField('Add new Picture')


def picture_form_id(product_id):
    class PictureFormID(PictureForm):
        pass

    PictureFormID.product_id = IntegerField('Product ID', validators=[DataRequired()], default=product_id)
    PictureFormID.picture = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    PictureFormID.title = StringField('Title', validators=[Length(max=32)])
    PictureFormID.submitpicture = SubmitField('Add new Picture')

    return PictureFormID()


class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), Length(min=1)])
    thumbnail = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png']), DataRequired()])
    submitproduct = SubmitField('Add new Product')


class ApplyChangesForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    apply = SubmitField('Apply Changes')


class DeleteProductForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()], default=0)
    confirm = BooleanField('Delete this product', validators=[DataRequired(), CheckboxCheck()])
    delete = SubmitField('Delete product')


def delete_product_id(product_id):
    class DeleteProductID(DeleteProductForm):
        pass

    DeleteProductID.product_id = IntegerField('Product ID', validators=[DataRequired()], default=product_id)
    DeleteProductID.confirm = BooleanField('Delete this product', validators=[DataRequired(), CheckboxCheck()])
    DeleteProductID.delete = SubmitField('Delete product')

    return DeleteProductID()


class DeletePictureForm(FlaskForm):
    picture_path = StringField("Product Name", validators=[DataRequired()], default='')
    submit = SubmitField('Delete picture')


def delete_picture_form(path):
    class DeletePicture(DeletePictureForm):
        pass

    DeletePicture.picture_path = StringField("Picture path", validators=[DataRequired()], default=path)

    return DeletePicture()


class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=32)])
    author = StringField("Author", validators=[DataRequired(), Length(min=2, max=32)], default='admin')
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=1)])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Create new post')


def new_blog_post(author):
    class BlogPostFormAuthor(BlogPostForm):
        pass

    BlogPostFormAuthor.author = StringField("Author", validators=[DataRequired(), Length(min=2, max=32)],
                                            default=author)
    return BlogPostFormAuthor()


class DeleteBlogPostForm(FlaskForm):
    post_id = IntegerField('Post id', default=0)
    delete_post = SubmitField('Delete this post')


def delete_blog_post_form_id(post_id):
    class DeleteBlogPostFormID(DeleteBlogPostForm):
        pass

    DeleteBlogPostFormID.post_id = IntegerField('Post id', default=post_id)
    return DeleteBlogPostFormID()

class EditBlogPostForm(FlaskForm):
    post_id = IntegerField('Post id', default=0)
    edit = SubmitField('Edit this post')


def edit_blog_post_form_id(post_id):
    class EditBlogPostFormID(EditBlogPostForm):
        pass

    EditBlogPostFormID.post_id = IntegerField('Post id', default=post_id)
    return EditBlogPostFormID()

def edit_blog_post(post):
    class BlogPostFormID(BlogPostForm):
        pass
    BlogPostFormID.title = StringField('Title', validators=[DataRequired(), Length(min=1, max=32)], default=post.title)
    BlogPostFormID.author = StringField("Author", validators=[DataRequired(), Length(min=2, max=32)], default=post.author)
    BlogPostFormID.content = TextAreaField('Content', validators=[DataRequired(), Length(min=1)], default=post.content)
    BlogPostFormID.submit = SubmitField(f'Edit post: {post.title}')
    return BlogPostFormID()