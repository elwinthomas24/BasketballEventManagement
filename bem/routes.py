from flask.helpers import flash
from flask_bcrypt import check_password_hash
from bem import app
from flask import render_template, redirect, url_for, request
from bem.models import Events, Teams, registrations
from bem import db
from bem.forms import CancelRegisterForm, RegisterForm, LoginForm, RegisterEventForm, CancelRegisterForm
from bem import db
from flask_login import login_user,logout_user, login_required, current_user

@app.route('/')
@app.route('/home',methods= ['GET','POST'])
def home_page():
    return render_template('home.html')

@app.route('/events', methods = ['GET','POST'])
@login_required
def events_page():
    # for event in current_user.register:
    #     print(event)
    
    register_event_form = RegisterEventForm()
    cancel_register_form = CancelRegisterForm()
    if register_event_form.validate_on_submit():
        if request.method == 'POST':
            #Register event logic
            registered_event = request.form.get('registered_event')
            r_event_object = Events.query.filter_by(id=registered_event).first()
            if r_event_object:
                r_event_object.register_for_event(current_user)
                flash(f"Successfully registered for event at {r_event_object.location}! Looking forward to seeing you there {current_user.teamname}.", category='success')
            

            #cancel registration logic
            cancelled_event = request.form.get('cancelled_event')
            c_event_object = Events.query.filter_by(id = cancelled_event).first()
            print(c_event_object)
            if c_event_object:
                c_event_object.registered_team.remove(current_user)
                db.session.commit()
            
            return redirect(url_for('events_page'))

    if request.method == "GET":
        # li = []
        # li = current_user.register
        user_r_events = current_user.register     #all events which current user has registered for 
        events_all = Events.query.all()            # querying all events
        events = [x for x in user_r_events + events_all if x not in user_r_events or x not in events_all]   # displaying only events which user hasnt registered for yet in upcoming section
        # print(events)
        
        return render_template('events.html', events = events, register_event_form = register_event_form, user_r_events = user_r_events, cancel_register_form = cancel_register_form)

@app.route('/maps', methods = ['GET','POST'])
# @login_required
def maps_page():
    events = Events.query.all()
    return render_template('maps.html', events = events)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        team_to_create  = Teams(teamname=form.teamname.data,
                                captain=form.captain.data,
                                j1=form.j1.data,
                                player_2= form.player2.data,
                                j2=form.j2.data,
                                player_3=form.player3.data,
                                j3=form.j3.data,
                                password=form.password1.data)
        if(team_to_create.j1 == team_to_create.j2 or team_to_create.j2 == team_to_create.j3 or team_to_create.j3 == team_to_create.j1):
            flash('Jersey numbers must be unique',category='danger')
        else:
            db.session.add(team_to_create)
            db.session.commit()
            login_user(team_to_create)
            flash(f'Account created successfully! You are now logged in as {team_to_create.teamname}', category = 'success')

            return redirect(url_for('events_page'))
    if form.errors != {}:   #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the team: {err_msg}', category = 'danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_team = Teams.query.filter_by(teamname =form.teamname.data).first()
        if attempted_team and attempted_team.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_team)
            flash(f'Success! You are logged in as:  {attempted_team.teamname}', category = 'success')
            return redirect(url_for('events_page'))
        else:
            flash(f'Team Name and Password do not match! Please try again', category = 'danger')    
    return render_template('login.html', form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    # flash("You have been logged out!", category ='info')
    return redirect(url_for('home_page'))

@app.route('/about')
def aboutUsPage():
    return render_template('aboutUs.html')

