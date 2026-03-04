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


@app.route('/info')
def info():
    return render_template('html/ex_info.html')


@app.route('/contacts')
def contacts():
    return render_template('html/contacts.html')


if __name__ == "__main__":
    app.run(port=8000)
