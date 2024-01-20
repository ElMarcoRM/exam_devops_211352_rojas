from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import MetaData, create_engine, text
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from os import getenv
from config import CONFIG
from flask_login import LoginManager, login_user, logout_user, login_required

app = Flask(__name__)

application = app
load_dotenv('.env' if getenv('ENV') == 'production' else '../.env')
app.config.from_object(CONFIG)

# БД
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
# print(environ)
print(app.config)

# Создание базы данных при первичном запуске
with create_engine(app.config['MYSQL_ENGINE_URI']).connect() as connection:
    connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {app.config['DB_NAME']}"))

migrate = Migrate(app, db)

from models import *
create_models(app)

@app.route('/add_data')
def add_data():
    event1 = Events(year=2018, date='15 февраля', desc='Рождение 10000 жителя города')
    db.session.add(event1)
    db.session.commit()

    event2 = Events(year=1951, date='1 июня', desc='Открытие сталепрокатного завода')
    db.session.add(event2)
    db.session.commit()

    event3 = Events(year=1812, date='30 октября', desc='Освобождение от войск Наполеона')
    db.session.add(event3)
    db.session.commit()

    event4 = Events(year=1789, date='1 октября', desc='Первое упоминание о городе')
    db.session.add(event4)
    db.session.commit()

    user1 = Workers(name='Андрей',login='aobugin',status='Работает')
    user1.set_password('qwerty1234')
    db.session.add(user1)
    db.session.commit()

    user2 = Workers(name='Дмитрий',login='dmrukole',status='Уволен')
    user2.set_password('aebc19kl')
    db.session.add(user2)
    db.session.commit()

    user3 = Workers(name='Денис',login='dbshafran',status='Работает')
    user3.set_password('qcvk13091')
    db.session.add(user3)
    db.session.commit()
    return redirect(url_for("index"))

# Главная страница и просмотр события
@app.route('/')
def index():
    information = {}
    if request.method == 'POST':
        year = request.form.get('year')
        information['year'] = year
        events = get_event_year(year)
    return render_template('index.html', events=events, information=information)

# Количество сотрудников 
@app.route('/count_employees')
@login_required
def employees():
    count_employees = count_not_fired()
    return render_template('employees.html', count_employees=count_employees)

# Авторизация
def load_user(user_id):
    user = db.session.execute(db.select(Workers).filter_by(id=user_id)).scalar()
    return user

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Для доступа к данной странице необходимо пройти процедуру аутентификации.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)

init_login_manager(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    information = {}
    if request.method == 'POST':
        login = request.form.get('loginInput')
        password = request.form.get('passwordInput')
        information["login"] = login
        information["password"] = password
        remember_me = request.form.get('remember_me') == 'on'
        if login and password:
            user = db.session.execute(db.select(Workers).filter_by(login=login)).scalar()
            if user and user.check_password(password):
                login_user(user, remember=remember_me)
                flash('Вы успешно аутентифицированы.', 'success')
                next = request.args.get('next')
                return redirect(next or url_for('index'))
        flash('Введены неверные логин и/или пароль.', 'danger')
    return render_template('login.html', information=information)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))



