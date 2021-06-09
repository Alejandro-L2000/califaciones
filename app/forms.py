from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class CursoForm(FlaskForm):
    name = StringField("Name of course", validators=[DataRequired()])
    submit = SubmitField("Register course")

class TareaForm(FlaskForm):
    titulo = StringField("Titulo", validators=[DataRequired()])
    fecha_de_creacion = DateTimeField("Fecha de Creación",format='%d-%m-%Y %H:%M:%S')
    fecha_de_entrega = DateTimeField("Fecha de Entrega",format='%d-%m-%Y %H:%M:%S')
    descripcion = StringField("Descripcion")
    puntos = IntegerField()
    submit = SubmitField("Registrar Tarea")