from flask import Flask
from flask import render_template, redirect, request, jsonify, json
from back.data.models.users_model import UserModel
from back.data.models.order_model import OrderModel
from back.forms.user_form import RegisterForm, LoginForm
from back.data import db_session

from flask_login import LoginManager
from flask_login import login_user, login_required, logout_user, current_user

import datetime

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
    })


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
        })
    return jsonify({'authenticated': False})


@app.route('/create_order', methods=['POST'])
@login_required
def create_order():
    """Создание нового заказа"""
    try:
        data = request.get_json()
        address = data.get('address')
        date_str = data.get('datetime')
        weight = data.get('weight')
        description = data.get('description', '')

        if not address or not date_str or not weight:
            return jsonify({
                'success': False,
                'message': 'Заполните все обязательные поля'
            }), 400

        try:
            weight = int(weight)
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Вес должен быть целым числом'
            }), 400

        try:
            order_date = datetime.datetime.fromisoformat(date_str)
        except ValueError:
            return jsonify({
                'success': False,
                'message': 'Неверный формат даты'
            }), 400

        session = db_session.create_session()

        order = OrderModel(
            user_id=current_user.id,
            address=address,
            date=order_date,
            weight=weight,
            description=description,
            is_active=True
        )

        session.add(order)
        session.commit()

        return jsonify({
            'success': True,
            'message': 'Заказ успешно создан!',
            'redirect': '/delivery'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Ошибка при создании заказа: {str(e)}'
        }), 500


@app.route('/get_active_orders')
@login_required
def get_active_orders():
    """Получение активных заказов текущего пользователя"""
    session = db_session.create_session()
    orders = session.query(OrderModel).filter(
        OrderModel.user_id == current_user.id,
        OrderModel.is_active == True
    ).order_by(OrderModel.date).all()

    return jsonify({
        'success': True,
        'orders': [order.to_dict() for order in orders]
    })


@app.route('/get_orders_history')
@login_required
def get_orders_history():
    """Получение истории заказов (выполненных)"""
    session = db_session.create_session()
    orders = session.query(OrderModel).filter(
        OrderModel.user_id == current_user.id,
        OrderModel.is_active == False
    ).order_by(OrderModel.created_at.desc()).all()

    return jsonify({
        'success': True,
        'orders': [order.to_dict() for order in orders]
    })


@app.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Отмена активного заказа"""
    session = db_session.create_session()
    order = session.query(OrderModel).filter(
        OrderModel.id == order_id,
        OrderModel.user_id == current_user.id,
        OrderModel.is_active == True
    ).first()

    if not order:
        return jsonify({
            'success': False,
            'message': 'Заказ не найден или уже выполнен'
        }), 404

    session.delete(order)
    session.commit()

    return jsonify({
        'success': True,
        'message': 'Заказ успешно отменен'
    })


@app.route('/complete_order/<int:order_id>', methods=['POST'])
@login_required
def complete_order(order_id):
    """Завершение заказа (для администратора или автоматически)"""
    session = db_session.create_session()
    order = session.query(OrderModel).filter(
        OrderModel.id == order_id,
        OrderModel.is_active == True
    ).first()

    if not order:
        return jsonify({
            'success': False,
            'message': 'Заказ не найден'
        }), 404

    order.is_active = False
    session.commit()

    return jsonify({
        'success': True,
        'message': 'Заказ выполнен'
    })


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
    return render_template('html/information.html', info=info_list)


def main():
    db_session.global_init('db.sqlite')
    app.run(port=80, host='0.0.0.0')


if __name__ == "__main__":
    main()
