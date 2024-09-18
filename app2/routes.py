from flask import render_template
from app import app  # Импортируем приложение после его создания

@app.route('/')
def index():
    return render_template('index.html')
