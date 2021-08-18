from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User


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
    picture = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    title = StringField('Title', validators=[DataRequired()])
    submitpicture = SubmitField('Add new Picture')

def picture_form_id(product_id):

    class PictureFormID(PictureForm):
        pass

    PictureFormID.product_id = IntegerField('Product ID', validators=[DataRequired()], default=product_id)
    PictureFormID.picture = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    PictureFormID.title = StringField('Title', validators=[DataRequired()])
    PictureFormID.submitpicture = SubmitField('Add new Picture')

    return PictureFormID()



class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    thumbnail = FileField(validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submitproduct = SubmitField('Add new Product')

class ApplyChangesForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Apply Changes')