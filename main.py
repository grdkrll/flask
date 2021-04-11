from flask import Flask, render_template
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime

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
    print(param['team_leaders'])
    return render_template("index.html", param=param)


if __name__ == '__main__':
    main()
