from flask import Flask, redirect, render_template, url_for
from flask import request

from forms import SnilsForm

from get_mesto import GetMesto

from variables import secret_key

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = secret_key # секрктный код в переменной окружения

@app.route('/', methods=['get', 'post'])
def index():

    form = SnilsForm()
    if form.validate_on_submit():
        snils = form.snils.data
        res = redirect(url_for('your_place'))
        res.set_cookie('snils', snils, max_age=60*60*24*7*4)
        print(snils)
        return res

    return render_template('test_template.html', form=form)


@app.route('/your_place/')
def your_place():
    snils = request.cookies.get('snils')
    mesto_obj = GetMesto('')
    mesto_obj.set_snils(snils)
    mesta = mesto_obj.get_mesto()

    return render_template('mesta.html', mesta=mesta)

@app.route('/napr/<napr_id>')
def napravlenie(napr_id):
    return 'napravlenie'

if __name__ == "__main__":
    app.run()