from flask import Blueprint

news_bp = Blueprint('news', __name__)

@news_bp.route('/')
def news():
    return '<h1>Новости в разработке</h1>'
