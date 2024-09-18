from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'password':  
            flash('Успешный вход', 'success')
            return redirect(url_for('index'))
        else:
            flash('Неправильное имя пользователя или пароль', 'danger')
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        flash('Регистрация успешна!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')
