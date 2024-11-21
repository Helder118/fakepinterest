# criar os formularios do site
from fakepinterest.models import Usuario
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class Formlogin(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    senha = PasswordField('senha', validators=[DataRequired()])
    botao = SubmitField('fazer login')



class Formcriarconta(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    nome = StringField('nome de usuario', validators=[DataRequired()])
    senha = PasswordField('senha', validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField('confirmacao da senha', validators=[DataRequired(), EqualTo('senha')])
    botao = SubmitField('criar conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('email ja cadastrado faca login para continuar')


class Formfoto(FlaskForm):
    foto = FileField("foto", validators=[DataRequired()])
    botao = SubmitField("carregar")