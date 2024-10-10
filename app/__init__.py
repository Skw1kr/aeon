from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Импортируем и регистрируем блюпринты
from .auth.routes import auth_bp
from .news.routes import news_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(news_bp, url_prefix='/news')