from flask import Flask
from flask import render_template
from back.forms.user_form import RegisterForm, LoginForm
from back.data import db_session

# DB
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'GrEEn_L1ne_S4creTT_K7Y'
app_manager = LoginManager()
app_manager.init_app(app)


@app.route('/')
@app.route('/index')
def index():
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


@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()
    print('anus')


@app.route('/auth',  methods=['POST'])
def auth():
    form = LoginForm()


def main(): # Запуск таблицы
    db_session.global_init('database/users.sqlite')
    app.run(port=8000)


if __name__ == "__main__":
    main()
