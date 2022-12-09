import os
from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import db
from user import User



#app config
DEBUG = True
SECRET_KEY = 'imagay'
app = Flask(__name__)
app.config.from_object(__name__)
login_manager = LoginManager(app)

# what to say and to where redirect when unauth person trying to visit somethig special
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(email):
    return User().init_by_email(email)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    return render_template('start.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))

    if request.method == 'POST':
        email = request.form['email']
        user_dict = db.get_user_by_email(email)
        print(user_dict)
        remember = True if request.form.get('remainme') else False
        if user_dict and check_password_hash(user_dict['password'], request.form['password']):
            login_user(User().init_by_dict(user_dict), remember=remember, fresh=False)
            return redirect(request.args.get('next') or url_for('main'))
        else:
            flash('Неверный логин/пароль', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        if len(request.form['email']) > 0 and len(request.form['psw']) > 0:
            hash = generate_password_hash(request.form['psw'])
            db.add_user(request.form['name'],
            request.form['surname'],
            request.form['address'],
            request.form['email'],
            request.form['passport'],
            request.form['phone'],
            request.form['status'],
            hash)
            return redirect(url_for('login'))
        else:
            flash("Неверно заполнены поля", "error")
    return render_template("signup.html", statuses=db.get_statuses())


@app.route('/main')
@login_required
def main():
    me = current_user.get_user()
    print(me)
    return render_template("myself.html",
    me=me,
    status=db.get_status(me['idStatus']),
    incomes=db.get_incomes(me['id']),
    expenses=db.get_expenses(me['id']))



@app.route('/income/<id>', methods=["POST", "GET"])
@login_required
def income(id):
    if request.method == "POST":
        db.delete_income(id)
        return redirect(url_for('main'))
    return render_template("income.html", income=db.get_income(id))

@app.route('/expense/<id>', methods=["POST", "GET"])
@login_required
def expense(id):
    if request.method == "POST":
        db.delete_expense(id)
        return redirect(url_for('main'))
    return render_template("expense.html", expense=db.get_expense(id))



@app.route('/add_income', methods=["POST", "GET"])
@login_required
def add_income():
    if request.method == "POST":
        source_id = db.get_source_id(request.form['status'])
        db.add_income(
            current_user.get_user()['id'],
            source_id,
            request.form['value'],
            request.form['desc']
        )
        return redirect(url_for('main'))
    return render_template('add_income.html', sources=db.get_sources())

@app.route('/add_expense', methods=["POST", "GET"])
@login_required
def add_expense():
    if request.method == "POST":
        db.add_expense(
            current_user.get_user()['id'],
            request.form['country'],
            request.form['value'],
            request.form['desc'],
        )
        return redirect(url_for('main'))
    return render_template('add_expense.html')


if __name__ == "__main__":
    app.run(debug=True)
