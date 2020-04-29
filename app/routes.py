from flask import render_template, flash, redirect, url_for, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm
from app.models import Users
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/", methods=['GET']) 
def home(): 
        return render_template('home.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pswd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Add user to database
        user = Users(username=form.username.data, pswd=hashed_pswd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form=form)


@app.route("/login/", methods=['GET', 'POST']) 
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.pswd, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/profile/", methods=['GET', 'POST']) 
@login_required
def profile():
        form = UpdateProfileForm()
        if form.validate_on_submit():
            current_user.temp = form.temp.data
            current_user.screen = form.screen.data
            current_user.room = form.room.data
            db.session.commit()
            flash('Your preferences has been updated!', 'success')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.temp.data = current_user.temp
            form.screen.data = current_user.screen
            form.room.data = current_user.room
            form.hours.data = current_user.hours
        return render_template('profile.html', title="Profile", form=form)

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/todolist/")
@login_required
def todolist():
    return render_template('todo.html')
