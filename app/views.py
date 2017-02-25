from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, EditUserForm
from .models import User
from  datetime import datetime


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return redirect(url_for('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return temp_login(email=form.email.data)
    return render_template('login.html', title='Sign In', form=form)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


def temp_login(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(nickname=email.split('@')[0], email=email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_connected = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user')
@login_required
def user():
    user = g.user
    accounts = [
        { 'name':'wallet', 'balance': 382, 'user': user},
        {'name':'bank', 'balance': -80, 'user': user}
    ]
    return render_template('user.html', user=user, accounts=accounts)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditUserForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    else:
        form.nickname.data = g.user.nickname
    return render_template('edituser.html', form=form)
