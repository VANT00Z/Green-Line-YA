from flask import Flask
from flask import render_template


app = Flask(__file__)


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


if __name__ == "__main__":
    app.run(port=8000, debug=True)
