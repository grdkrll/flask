from datetime import datetime
from flask import Flask, render_template, redirect
from flask.helpers import flash
from data import db_session
from data.users import User
from data.jobs import Jobs
from data.register_form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/data.db")
    db_sess = db_session.create_session()
    app.run(port=8080)

@app.route("/")
def index():
    param = {}
    db_sess = db_session.create_session()
    param['activities'] = db_sess.query(Jobs).all()
    param['team_leaders'] = []
    for a in param['activities']:
        param['team_leaders'].append(db_sess.query(User).filter(User.id == a.team_leader).first())
    return render_template("index.html", param=param)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.rpassword.data:
            flash('Repeat the same password')
        else:
            user = User()
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.position = form.position.data
            user.speciality = form.speciality.data
            user.address = form.address.data
            user.email = form.email.data
            user.hashed_password = hash(form.password.data)
            user.modified_date = datetime.now()
            db_sess = db_session.create_session()
            db_sess.add(user)
            db_sess.commit()
            return redirect('/')
    param={}
    return render_template('register.html', param=param, form=form)


if __name__ == '__main__':
    main()
