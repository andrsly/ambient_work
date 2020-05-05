from flask import render_template, flash, redirect, url_for, request
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, UpdateProfileForm, DrinkForm, EatForm
from app.models import Users
from flask_login import login_user, current_user, logout_user, login_required
import datetime


@app.route("/", methods=['GET', 'POST']) 
def home(): 
    dform = DrinkForm()
    eform = EatForm()
    if eform.validate_on_submit():
            current_user.food =  current_user.food + eform.food.data
            db.session.commit()
            return redirect(url_for('home'))
    elif dform.validate_on_submit():
            current_user.liquids = current_user.liquids + dform.liquids.data
            db.session.commit() 
            return redirect(url_for('home'))
    elif request.method == 'GET':
        dform.liquids.data = 0.2
        eform.food.data = 1
    return render_template('home.html', title='Home', dform=dform, eform=eform)

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
            # Add login time to database
            user.login_time = datetime.datetime.utcnow()
            user.liquids = 0.0
            user.food = 0
            db.session.commit()
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
            current_user.hours = form.hours.data
            current_user.work_minutes = form.work_minutes.data
            current_user.pause_minutes = form.pause_minutes.data
            db.session.commit()
            flash('Your preferences has been updated!', 'success')
            return redirect(url_for('profile'))
        elif request.method == 'GET':
            form.temp.data = current_user.temp
            form.screen.data = current_user.screen
            form.room.data = current_user.room
            form.hours.data = current_user.hours
            form.work_minutes.data = current_user.work_minutes
            form.pause_minutes.data = current_user.pause_minutes
        return render_template('profile.html', title="Profile", form=form)

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/todolist/")
@login_required
def todolist():
    return render_template('todo.html')

@app.route("/test/")
@login_required
def test():
    return render_template('test.html')


    