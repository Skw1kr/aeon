import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('fckdtbs.db')
    conn.row_factory = sqlite3.Row
    return conn

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Подключение к базе данных и проверка пользователя
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE login = ? AND password = ?', (username, password)).fetchone()
        conn.close()

        if user:
            # Если пользователь найден, сохраняем его в сессии и перенаправляем на профиль
            session['username'] = username
            return redirect(url_for('auth.profile'))
        else:
            # Остаемся на странице логина, если пользователь не найден
            return render_template('login.html', error="Неверное имя пользователя или пароль")

    return render_template('login.html')


@auth_bp.route('/profile')
def profile():
    # Проверяем, вошел ли пользователь
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # Показываем профиль пользователя
    username = session['username']
    return render_template('profile.html', username=username)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Подключение к базе данных и добавление пользователя
        conn = get_db_connection()
        conn.execute('INSERT INTO users (login, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    # Удаляем пользователя из сессии
    session.pop('username', None)
    return redirect(url_for('auth.login'))
