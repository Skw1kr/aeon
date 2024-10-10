import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

# подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('fckdtbs.db')
    conn.row_factory = sqlite3.Row  # для удобного обращения к колонкам по именам
    return conn

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['login']  
            return redirect(url_for('auth.profile'))  
        else:
            flash('Неправильный логин или пароль')  
            return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))  
    
    user_id = session['user_id']  
  
    conn = get_db_connection()
    
    user_data = conn.execute("SELECT login, balance FROM users WHERE login = ?", (user_id,)).fetchone()
    conn.close()

    if user_data:
        username, balance = user_data['login'], user_data['balance']  
        return render_template('profile.html', username=username, balance=balance)
    else:
        return "User not found", 404


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # подключение к базе данных и добавление пользователя
        conn = get_db_connection()
        conn.execute('INSERT INTO users (login, password, balance) VALUES (?, ?, ?)', (username, password, 1000.0))
        conn.commit()
        conn.close()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    # удаляем пользователя из сессии
    session.pop('user_id', None)  # удаляем user_id из сессии
    return redirect(url_for('auth.login'))
