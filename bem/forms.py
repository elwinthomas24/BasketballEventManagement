from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField , PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from bem.models import Teams


class RegisterForm(FlaskForm):

    def validate_teamname(self, teamname_to_check):
        team = Teams.query.filter_by(teamname=teamname_to_check.data).first()
        if team:
            raise ValidationError('Team Name already exists! Please try a different Team Name')

    def validate_j1(self, j1_to_check):
        jersey1 = Teams.query.filter_by(j1=j1_to_check.data).first()
        if jersey1:
            raise ValidationError(f'Jersey Number {jersey1.j1} is already taken! Please try a different Jersey Number')

    def validate_j2(self, j2_to_check):
        jersey2 = Teams.query.filter_by(j2=j2_to_check.data).first()
        if jersey2:
            raise ValidationError(f'Jersey Number {jersey2.j2} is already taken! Please try a different Jersey Number')

    def validate_j3(self, j3_to_check):
        jersey3 = Teams.query.filter_by(j3=j3_to_check.data).first()
        if jersey3:
            raise ValidationError(f'Jersey Number {jersey3.j3} is already taken! Please try a different Jersey Number')

    

    teamname = StringField(label='Team Name', validators=[Length(min=2, max=20), DataRequired()])
    captain = StringField(label='Team Captain', validators=[DataRequired()])
    j1 = StringField(label='Jersey No',validators=[DataRequired()])
    player2 = StringField(label='Player 2',validators=[DataRequired()])
    j2 = StringField(label='Jersey No',validators=[DataRequired()])
    player3 = StringField(label='Player 3',validators=[DataRequired()])
    j3 = StringField(label='Jersey No',validators=[DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label= 'CREATE ACCOUNT')

class LoginForm(FlaskForm):
    teamname = StringField(label='Team Name',validators=[DataRequired()])
    password = PasswordField(label='Password',validators=[DataRequired()])
    submit = SubmitField(label= 'Sign In')

class RegisterEventForm(FlaskForm):
    submit = SubmitField(label = 'Register')

class CancelRegisterForm(FlaskForm):
    submit = SubmitField(label = 'Cancel Registration')