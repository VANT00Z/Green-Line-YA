from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, IntegerField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional

class DeliveryForm(FlaskForm):
    adress = StringField('Адрес', validators=[DataRequired()])
    date = DateTimeField('Дата и время', validators=[DataRequired()])
    weight = IntegerField('Вес', validators=[Optional()])
    description = TextAreaField('Описание', validators=[])
    active = BooleanField('Активный заказ')
    submit = SubmitField('Создать заказ')