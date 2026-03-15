from flask import Flask
from flask import render_template
from back.forms.user_form import RegisterForm, LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'GrEEn_L1ne_S4creTT_K7Y'


@app.route('/')
@app.route('/main')
def main():
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


@app.route('/auth',  methods=['POST'])
def auth():
    form = LoginForm()


if __name__ == "__main__":
    app.run(port=8000)