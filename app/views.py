from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'stan'}
    categories = [
        {
            'name':'Food',
            'left': 123
        },
        {
            'name':'Entertainment',
            'left':0 #QQ
        }
    ]
    return render_template('index.html',title='Home', user=user, categories=categories)
