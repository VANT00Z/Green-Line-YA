from flask import Flask
from flask import render_template, redirect, request, jsonify, json
from back.data.models.users_model import UserModel
from back.data.models.order_model import OrderModel
from back.forms.user_form import RegisterForm, LoginForm
from back.data import db_session


from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'GrEEn_L1ne_S4creTT_K7Y'
app_manager = LoginManager()
app_manager.init_app(app)
app_manager.login_view = 'index'


@app_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.get(UserModel, user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    session = db_session.create_session()
    user = session.query(UserModel).filter(
        UserModel.email == email).first()

    if user and user.check_password(password):
        login_user(user)
        return jsonify({
            'success': True,
            'message': 'Успешный вход!',
            'redirect': '/delivery'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Неправильный email или пароль'
        }), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    surname = data.get('surname')
    email = data.get('email')
    password = data.get('password')
    rep_password = data.get('rep_password')

    if not all([name, surname, email, password, rep_password]):
        return jsonify({
            'success': False,
            'message': 'Все поля обязательны для заполнения'
        }), 400

    if password != rep_password:
        return jsonify({
            'success': False,
            'message': 'Пароли не совпадают'
        }), 400

    if len(password) < 6:
        return jsonify({
            'success': False,
            'message': 'Пароль должен содержать не менее 6 символов'
        }), 400

    session = db_session.create_session()

    if session.query(UserModel).filter(UserModel.email == email).first():
        return jsonify({
            'success': False,
            'message': 'Пользователь с таким email уже существует'
        }), 400

    user = UserModel(
        name=name,
        surname=surname,
        email=email
    )
    user.set_password(password)
    session.add(user)
    session.commit()

    login_user(user)

    return jsonify({
        'success': True,
        'message': 'Регистрация успешно завершена!',
        'redirect': '/delivery'
    }), 400


@app.route('/check_auth')
def check_auth():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'name': current_user.name,
                'surname': current_user.surname,
                'email': current_user.email
            }
        }), 400
    return jsonify({'authenticated': False})


@app.route('/order', methods=['POST'])
def make_order():
    data = request.json()
    adress = data.get('adres')
    date = data.get('date')
    weight = data.get('weight')
    description = data.get('description')

    if not all(adress, date, weight):
        return jsonify({
            'success': False,
            'message': 'Не все обязательные поля заполены'
        })

    if isinstance(weight, int):
        return jsonify({
            'success': False,
            'message': 'Вес должен быть целочисленным'
        })

    session = db_session.create_session()

    order = OrderModel(
        adress=adress,
        date=date,
        weight=weight,
        description=description
    )

    session.add(order)
    session.commit()


@app.route('/orders_history')
@login_required
def get_history():
    session = db_session.create_session()


@app.route('/')
@app.route('/index')
def index():
    return render_template('html/index.html')


@app.route('/delivery')
@login_required
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
    with open('static/json/info.json', 'rt', encoding='utf-8') as file:
        info_list = json.loads(file.read())
    print(info_list)
    return render_template('html/information.html', info=info_list)


def main():
    db_session.global_init('db.sqlite')
    app.run(port=8000, debug=True)


if __name__ == "__main__":
    main()
