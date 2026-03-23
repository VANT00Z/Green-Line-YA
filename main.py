from flask import Flask
from flask import render_template, redirect
from back.data.models.users_model import UserModel
from back.data.models.order_model import OrderModel
from back.forms.user_form import RegisterForm, LoginForm
from back.data import db_session

# DB
from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'GrEEn_L1ne_S4creTT_K7Y'
app_manager = LoginManager()
app_manager.init_app(app)


@app_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(UserModel, user_id)


@app_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(UserModel)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(UserModel).filter(
            UserModel.email == form.mail.data).first()
        if user and user.check_password(form.password.data):
            return redirect("/delivery")
        return redirect("/")    # Переадресовка: неправильный пароль или логин
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.ex_password.data:
            return redirect('/index')   # Переадресовка: повтор пароля неверный
        session = db_session.create_session()
        if session.query(UserModel).filter(UserModel.email == form.mail.data).first():
            return ("/index")   # Переадресовка: Пользователь уже есть
        user = UserModel(
            name=form.name.data,
            mail=form.mail.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/index')
    return redirect('/index')


@app.route('/')
@app.route('/index')
def index():
    session = db_session.create_session()
    return render_template('html/index.html')


@app.route('/delivery')
def delivery():
    return render_template('html/delivery.html')


@app.route('/ex-info')
def ex_info():
    return render_template('html/ex_info.html')


@app.route('/contacts')
def contacts():
    return render_template('html/contacts.html')


@app.route('/info')
def info():
    return render_template('html/information.html')


def main():
    db_session.global_init('db.sqlite')
    app.run(port=8000)


if __name__ == "__main__":
    main()
