from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField
from wtforms import BooleanField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Optional, Email, Length

class RegisterForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(), Length(min=3, max=30)])
    surname = StringField('Фаимилия', validators=[DataRequired(), Length(min=3, max=30)])
    mail = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    ex_password = PasswordField('Повтор пароля',validators=[DataRequired()])
    submit = SubmitField('Войти')



class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    mail = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
    
    
class DeliveryForm(FlaskForm):
    adress = StringField('Адрес', validators=[DataRequired()])
    date = DateTimeField('Дата и время', validators=[DataRequired()])
    weight = IntegerField('Вес', validators=[Optional()])
    description = TextAreaField('Описание', validators=[])
    active = BooleanField('')
    submit = SubmitField('Создать заказ')