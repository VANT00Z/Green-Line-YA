from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    " Форма регистрации "
    name = StringField('Имя', validators=[
                       DataRequired(), Length(min=3, max=30)])
    surname = StringField('Фамилия', validators=[
                          DataRequired(), Length(min=3, max=30)])
    mail = EmailField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[
                             DataRequired(), Length(min=6)])
    ex_password = PasswordField('Повтор пароля', validators=[DataRequired()])
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    " Форма авторизации "
    username = StringField('Логин', validators=[DataRequired()])
    mail = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')
