import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

# подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('fckdtbs.db')
    conn.row_factory = sqlite3.Row
    return conn

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        # подключение к базе данных и проверка пользователя
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['login']  # Сохранение логина пользователя в сессии
            return redirect(url_for('auth.profile'))  # Переадресация на страницу профиля
        else:
            flash('Неправильный логин или пароль')  # Сообщение об ошибке
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/profile')
def profile():
    # проверяем, есть ли пользователь в сессии
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Переадресация на страницу логина, если пользователь не авторизован
    
    # отображаем страницу профиля
    return render_template('profile.html', user=session['user_id'])

    # проверяем, вошел ли пользователь
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # показываем профиль пользователя
    username = session['username']
    return render_template('profile.html', username=username)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # подключение к базе данных и добавление пользователя
        conn = get_db_connection()
        conn.execute('INSERT INTO users (login, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    # удаляем пользователя из сессии
    session.pop('username', None)
    return redirect(url_for('auth.login'))
