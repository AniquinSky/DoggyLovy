import functools
import smtplib
import yagmail

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import flaskr.db as db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        personName = request.form['personName']
        gender = request.form['gender']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        birthDate = request.form['birthDate']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        error = None

        if not username:
            error = 'Nombre de usuario es necesario.'
        if not personName:
            error = 'Nombre completo es necesario.'
        if not email:
            error = 'Correo es necesario.'
        if not birthDate:
            error = 'Una fecha de nacimiento es necesaria'
        if not password:
            error = 'Contrasena es necesaria.'
        elif password != confirmPassword:
            error = 'La contrasena y confirmacion de contrasena no coinciden.'

        if error is None:
            connDB = db.get_db()
            cur = connDB.cursor()
            try:
                cur.execute(
                    "INSERT INTO usuario (id_usuario, nom_usuario, correo, password, telefono, fecha_nacimiento, genero) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (username, personName, email, generate_password_hash(password), phoneNumber, birthDate, gender),
                )
                connDB.commit()
                enviar_correo(email, username)
            except connDB.IntegrityError:
                error = f"El nombre de usuario {username} ya se encuentra ocupado."
            except Exception as e:
                print(e)
                error = "Ocurrio un error inesperado. Intentelo mas tarde."
            cur.close()
            db.close_db()
            # Cambiar para que redirija al home page
            return redirect(url_for("index"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connDB = db.get_db()
        cur = connDB.cursor()
        error = None
        cur.execute(
            "SELECT id_usuario, password FROM usuario WHERE id_usuario = %s",
            (username,)
        )
        user = cur.fetchone()
        cur.close()
        db.close_db()

        # Como medida de seguridad basica se muestra el mismo mensaje si el
        # nombre de usuario o contrasena son incorrectos.
        # Esto porque asi una persona con intenciones maliciosas no puede saber
        # cual de los dos datos esta mal.
        if user is None:
            error = 'Nombre de usuario o contrasena incorrecto.'
        elif not check_password_hash(user[1], password):
            error = 'Nombre de usuario o contrasena incorrecto.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        connDB = db.get_db()
        cur = connDB.cursor()
        cur.execute(
            'SELECT nom_usuario FROM usuario WHERE id_usuario = %s', (user_id,)
        )
        g.user = cur.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def enviar_correo(email, usuario):
    passToken = 'skhxvywqburocwjv'
    emailPage =     'doggylovy.contact@gmail.com'
    
    yag = yagmail.SMTP(user = emailPage, password = passToken)
    
    username= usuario
    destinatario = email
    asunto = 'Confirmacion de creacion de cuenta'
    html= """<!DOCTYPE html>
            <body>
                <h1>¡Gracias por registrarte!</h1>
                <p>Te damos la bienvenida a nuestro sitio. Estamos emocionados de tenerte como parte de nuestra comunidad.</p>
            </body>
            </html>
        """
    mensaje = 'Hola ' + username + ' tu cuenta fue creada con exito!!' + '\n' + html
    yag.send(destinatario, asunto, mensaje)
    yag.close()