from app import app, db
from app.models import User, EditHistory
from app.forms import LoginForm, RegistrationForm

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', category='error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration is successful. Please log in with your account.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/index')
@login_required
def index():
    return render_template("index.html")


@app.route("/history")
@login_required
def show_history():
    all_history = EditHistory.query.order_by(EditHistory.changed_time.desc()).all()
    return render_template("history.html", histories=all_history)


@app.route("/user")
@login_required
def show_user():
    all_user = User.query.order_by(User.id).all()
    return render_template("user.html", users=all_user)


@app.route("/user/delete/<id>", methods=['GET', 'POST'])
def delete_user(id):
    user_to_delete = User.query.filter_by(id=id).first()

    db.session.delete(user_to_delete)
    db.session.commit()
    flash("User account deleted successfully")

    return redirect(url_for('show_user'))
