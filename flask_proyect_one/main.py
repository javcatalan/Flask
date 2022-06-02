from cgitb import text
import email
from flask import Flask, redirect, url_for,flash 
from flask import render_template,session
from flask import request,make_response,g

from config import DevelopmentConfig

from models import db
from models import User
from models import Comment

from flask_wtf import CSRFProtect
import forms
import json


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['comment']:
        return redirect(url_for('login'))
    elif 'username' in session and request.endpoint in ['login','create']:
        return redirect(url_for('index'))

@app.route('/')
def index():
    #custome_cookie= request.cookies.get('custome_cookie','Undefined')
    if 'username' in session:
        username = session['username']
    #print(username)
    title = 'Index'
    return render_template('index.html', title = title)
    # comment_form = forms.CommentForm(request.form) 
    # if request.method == 'POST' and comment_form.validate():
    #     print (comment_form.username.data)
    #     print (comment_form.email.data)
    #     print (comment_form.comment.data)
    # else:
    #     print("Error en el formilario")

    # title = "Curso flask"
    # return render_template('index.html',title=title, form=comment_form)

@app.after_request
def after_request(response):
    return response

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect(url_for('login'))

@app.route('/create', methods=['GET','POST'])
def create():
    create_form = forms.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        user = User(create_form.username.data,
                    create_form.password.data,
                    create_form.email.data )

        db.session.add(user)
        db.session.commit()
    
        success_message = 'Usuario registrado en la base de datos'
        flash(success_message)
        print(user)

    return render_template('create.html', form = create_form)

@app.route('/cookie')
def cookie():
    response = make_response ( render_template ('cookie.html'))
    response.set_cookie('custome_cookie', 'javier')
    return response

@app.route('/login', methods=['POST','GET'])
def login():
    login_form= forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        id = login_form.id.data 

        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
           # user = User.query.filter_by(username = username).first()
            #id = login_form.id.data 

            session['username'] = username
            session['user_id'] = id 
            return redirect(url_for('index'))
        else:
            error_message = 'Usuario o contraseña no valida!'
            flash(error_message)

        session['username'] = login_form.username.data
        session['user_id'] = login_form.id.data
    return render_template('login.html', form = login_form)

@app.route('/comment', methods=['GET','POST'])
def comment():
   # user_id = User.query.filter_by(id = id).first()
    comment_form = forms.CommentForm(request.form)

    
    if request.method == 'POST' and comment_form.validate():
        #session['user_id'] = id
        user_id = session['user_id']
        comment = Comment(user_id = user_id ,
                            text = comment_form.comment.data)

        db.session.add(comment)
        db.session.commit()

        success_message = user_id,'Nuevo comentario creado'
        flash(success_message)

    title = "Curso Flask"
    return render_template('comment.html', title = title, form = comment_form)


@app.route('/ajax-login', methods=['POST'])
def ajax_login():
    print(request.form)
    username = request.form['username']
    response = {'status': 200, 'username': username, 'id':1}
    return json.dumps(response)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
     db.create_all()

    app.run(port=8000)



