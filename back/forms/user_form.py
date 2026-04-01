from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegisterForm(FlaskForm):
    " Форма регистрации "
    name = StringField('Имя', validators=[
        DataRequired(message='Имя обязательно'),
        Length(min=3, max=30,
               message='Имя должно быть от 3 до 30 символов')
    ])
    surname = StringField('Фамилия', validators=[
        DataRequired(message='Фамилия обязательна'),
        Length(min=3, max=30,
               message='Имя должно быть от 3 до 30 символов')
    ])
    mail = EmailField('Почта', validators=[
        DataRequired(),
        Email(message='Введите корректный email')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=6, message='Пароль должен быть не менее 6 символов')
    ])
    ex_password = PasswordField('Повтор пароля', validators=[DataRequired(message='Повторите пароль'),
                                                             EqualTo(
        'password', message='Пароли должны совпадать')
    ])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    " Форма авторизации "
    mail = EmailField('Почта', validators=[
                      DataRequired(message='Почта обязательна'), Email(message='Введите корректный email')])
    password = PasswordField('Пароль', validators=[
                             DataRequired(message='Пароль обязателен')])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
