from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, EmailField, PasswordField, IntegerField
from wtforms.validators import DataRequired, URL, EqualTo, Optional


class RegisterForm(FlaskForm):
    name = StringField("Nazwa Użytkownika", validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź Hasło', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Dodaj Użytkownika')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')


class SponsorForm(FlaskForm):
    img = FileField('Logo Sponsora', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png'])])
    name = StringField('Nazwa Sponsora', validators=[DataRequired()])
    website_url = StringField('Link do Strony Sponsora', validators=[URL(), Optional()])
    submit = SubmitField('Zapisz')


class ManagementForm(FlaskForm):
    name = StringField("Nazwa Członka Zarządu", validators=[DataRequired()])
    position = StringField("Stanowisko Członka Zarządu", validators=[DataRequired()])
    order = IntegerField('Pozycja na Stronie', validators=[DataRequired()])
    submit = SubmitField('Zapisz')


class TeamForm(FlaskForm):
    name = StringField('Nazwa Drużyny', validators=[DataRequired()])
    img = FileField('Zdjęcie Drużyny', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png'])])
    vintage = StringField('Roczniki', validators=[DataRequired()])
    trainer = StringField('Trener', validators=[DataRequired()])
    trainer_phone = StringField('Telefon Trenera')
    order = IntegerField('Pozycja na Stronie', validators=[DataRequired()])
    submit = SubmitField('Zapisz')


class ProjectForm(FlaskForm):
    img = FileField('Zdjęcie Projektu', validators=[FileRequired(), FileAllowed(['jpg','jpeg','png'])])
    name = StringField('Nazwa Projektu', validators=[DataRequired()])
    description = TextAreaField('Opis Projektu', validators=[DataRequired()])
    submit = SubmitField('Zapisz')

