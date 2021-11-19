
from flask_login import UserMixin
from bem import db
from bem import bcrypt
from bem import login_manager

@login_manager.user_loader
def load_user(user_id):
    return Teams.query.get(int(user_id))

registrations = db.Table('registrations',
    db.Column('team_id', db.Integer, db.ForeignKey('teams.team_id')),
    db.Column('event_id', db.Integer, db.ForeignKey('events.id'))
)

class Teams(db.Model, UserMixin):
    team_id = db.Column(db.Integer(), primary_key = True)
    teamname = db.Column(db.String(length = 30),nullable = False, unique = True)
    captain = db.Column(db.String(length = 30),nullable = False)
    j1 = db.Column(db.Integer(),nullable = False, unique = True)
    player_2 = db.Column(db.String(length = 30),nullable = False)
    j2 = db.Column(db.Integer(),nullable = False, unique = True)
    player_3 = db.Column(db.String(length = 30),nullable = False)
    j3 = db.Column(db.Integer(),nullable = False, unique = True)
    password_hash = db.Column(db.String(length = 60),nullable = False)
    register = db.relationship('Events', secondary = registrations, backref= db.backref('registered_team', lazy = 'dynamic'))

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
            
    def get_id(self):
        return (self.team_id)

    def __repr__(self):
        
        return f'{self.team_id}'

  

class Events(db.Model):
    id = db.Column(db.Integer(), primary_key = True)
    location = db.Column(db.String(length = 30),nullable = False)
    tournament_type = db.Column(db.String(),nullable = False)
    fee = db.Column(db.Integer(),nullable = False)
    description = db.Column(db.String(length = 1024))


    def __repr__(self):
        # return f'{self.location} {self.tournament_type}'
        return f'{self.id}'

    def register_for_event(self, user):
        self.registered_team.append(user)
        db.session.commit()
