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
        login = request.form['login']
        password = request.form['password']

        # подключение к базе данных и проверка пользователя
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password)).fetchone()
        conn.close()

        if user:
<<<<<<< HEAD
            session['user_id'] = user['login']  # Сохранение логина пользователя в сессии
            return redirect(url_for('auth.profile'))  # Переадресация на страницу профиля
        else:
            flash('Неправильный логин или пароль')  # Сообщение об ошибке
            return redirect(url_for('auth.login'))
=======
            # если пользователь найден, сохраняем его в сессии и перенаправляем на профиль
            session['username'] = username
            return redirect(url_for('auth.profile'))
        else:
            return render_template('login.html', error="Неверное имя пользователя или пароль")
>>>>>>> b753163718b5dd0193cb99e0dd6db80888cdf887

    return render_template('login.html')

@auth_bp.route('/profile')
def profile():
<<<<<<< HEAD
    # Проверяем, есть ли пользователь в сессии
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  # Переадресация на страницу логина, если пользователь не авторизован
    
    # Отображаем страницу профиля
    return render_template('profile.html', user=session['user_id'])

=======
    # проверяем, вошел ли пользователь
    if 'username' not in session:
        return redirect(url_for('auth.login'))
    
    # показываем профиль пользователя
    username = session['username']
    return render_template('profile.html', username=username)
>>>>>>> b753163718b5dd0193cb99e0dd6db80888cdf887


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
