from wtforms import Form
from wtforms import TextAreaField, StringField
from wtforms.fields import EmailField  
from wtforms import HiddenField, PasswordField
from wtforms import validators
from models import User

def lenght_honeypot(form,field):
    if len(field.data)> 0:
        raise validators.ValidationError('El campo debe de estar vacio.')

class CommentForm(Form):
    # username = StringField('username',
    # [
    #      validators.InputRequired(message='el usuario es requerido!.'),
    #      validators.length(min=4, max=25, message='ingrese un usuario valido')
    # ]   
    # )
    # email = EmailField('correo electronico',
    # [
    #     validators.InputRequired(message='el usuario es requerido!.'),
       ##validators.EqualTo(message='ingrese un email valido')

   # ])
    comment = TextAreaField('comentario')
    #honeypot = HiddenField('',[lenght_honeypot])

class LoginForm(Form):
    username = StringField('username',
    [
        validators.DataRequired(message= 'el username es requerido'),
        validators.length(min=4, max=25, message='ingrese un username valido'),
    
    ])
    password = PasswordField('Password', [validators.DataRequired(message='ingrese una contraseña valida')
    ])
    id = StringField('id')

class CreateForm(Form):
    username = TextAreaField('Username',
                [
                    validators.DataRequired(message= 'El username es requerido'),
                    validators.length(min=4, max=50, message='Ingrese un usuario valido')
                ])
    email = EmailField('Correo electronico',
            [
                validators.DataRequired(message= 'El email es requerido'),
            ])
    password = PasswordField('Password', [validators.DataRequired(message='ingrese una contraseña valida')
    ])

    def validate_username(form, field):
        username = field.data
        user = User.query.filter_by(username = username).first()
        if user is not None:
            raise validators.ValidationError('El usuario ya se encuentra registrado')
