from flask_wtf import FlaskForm
import wtforms.validators as v
import wtforms.fields as f


class LoginForm(FlaskForm):
    email = f.EmailField('Email', validators=[v.DataRequired()])
    password = f.PasswordField('Password', validators=[v.DataRequired()])
    remember_me = f.BooleanField('Remember Me')


class CustomerForm(FlaskForm):
    first = f.StringField('First', validators=[v.DataRequired()])
    last = f.SearchField('Last', validators=[v.DataRequired()])
    email = f.EmailField('Email', validators=[v.DataRequired()])
    gender = f.SelectField('Gender',
                           choices=[('', ''), ('male', 'Male'),
                                    ('female', 'Female')],
                           validate_choice=True)
    cell_phone = f.StringField('Cell Phone', validators=[v.DataRequired()])
    home_phone = f.StringField('Home Phone')
    address_1 = f.StringField('Street Address')
    address_2 = f.StringField('Lot / Unit')
    city = f.StringField('City')
    zipcode = f.numeric.IntegerField('Zipcode')
    alt_first = f.StringField('First', validators=[v.DataRequired()])
    alt_last = f.SearchField('Last', validators=[v.DataRequired()])
    alt_email = f.EmailField('Email', validators=[v.DataRequired()])
    alt_gender = f.SelectField('Gender',
                               choices=[('', ''), ('male', 'Male'),
                                        ('female', 'Female')],
                               validate_choice=True)
    alt_cell_phone = f.StringField('Cell Phone', validators=[v.DataRequired()])
    alt_home_phone = f.StringField('Home Phone')
