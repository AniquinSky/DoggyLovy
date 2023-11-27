import functools
import smtplib
import yagmail

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

import flaskr.db as db
from psycopg2 import Binary as to_binary

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        print(request.form)
        username = request.form['username']
        personName = request.form['personName']
        gender = request.form['gender']
        email = request.form['email']
        phoneNumber = request.form['phoneNumber']
        birthDate = request.form['birthDate']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        dni = request.files['dni']
        picImage = request.files['profile_pic']

        error = None

        if not username:
            error = 'Nombre de usuario es necesario.'
        if not personName:
            error = 'Nombre completo es necesario.'
        if not email:
            error = 'Correo es necesario.'
        if not birthDate:
            error = 'Una fecha de nacimiento es necesaria'
        if not dni:
            error = 'Foto de identificacion necesaria.'
        if not picImage:
            error = 'Foto de perfil necesaria.'
        if not password:
            error = 'Contrasena es necesaria.'
        elif password != confirmPassword:
            error = 'La contrasena y confirmacion de contrasena no coinciden.'

        if error is None:
            dniData = dni.read()
            picImageData = picImage.read()
            connDB = db.get_db()
            cur = connDB.cursor()
            try:
                cur.execute(
                    "INSERT INTO usuario (id_usuario, nom_usuario, correo, password, telefono, fecha_nacimiento, genero, dni, profile_pic, valid_cuenta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, default)",
                    (username, personName, email, generate_password_hash(password), phoneNumber, birthDate, gender, to_binary(dniData), to_binary(picImageData)),
                )
                connDB.commit()
                enviar_correo(email, username)
            except connDB.IntegrityError as e:
                print(e)
                if "usuario_pkey" in e.pgerror:
                    error = f"El nombre de usuario \"{username}\" ya se encuentra registrado."
                elif "correo_unico" in e.pgerror:
                    error = f"El correo electronico \"{email}\" ya se encuentra registrado."
                elif "telefono_unico" in e.pgerror:
                    error = f"El numero de telefono \"{phoneNumber}\" ya se encuentra registrado."
                else:
                    error = "El valor de uno de los campos ya se encuentra registrado."
            except Exception as e:
                print(e)
                error = "Ocurrio un error inesperado. Intentelo mas tarde."
            cur.close()
            db.close_db()

            if error is None:
                session.clear()
                session['user_id'] = username
                session['user_name'] = personName
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

        try:
            cur.execute(
                "SELECT id_usuario, password, nom_usuario, status FROM usuario WHERE id_usuario = %s",
                (username,)
            )
            user = cur.fetchone()
        except Exception as e:
            print(e)
            error = 'Ocurrio un error inesperado. Intentelo de nuevo mas tarde.'
        finally:
            cur.close()
            db.close_db()

        # Como medida de seguridad basica se muestra el mismo mensaje si el
        # nombre de usuario o contrasena son incorrectos.
        # Esto porque asi una persona con intenciones maliciosas no puede saber
        # cual de los dos datos esta mal.
        if error is not None:
            error = 'Ocurrio un error inesperado. Intentelo de nuevo mas tarde.'
        elif user is None:
            error = 'Nombre de usuario o contrasena incorrecto.'
        elif not check_password_hash(user[1], password):
            error = 'Nombre de usuario o contrasena incorrecto.'
        elif user[3] == 3:
            error = 'La cuenta está bloqueada.'

        if error is None:
            session.clear()
            session['user_id'] = user[0]
            session['user_name'] = user[2]
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = session.get('user_name')
        g.user_id = user_id
        g.pet_id = session.get('current_pet_id')
        g.pet_name = session.get('current_pet_name')

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
    emailPage = 'doggylovy.contact@gmail.com'
    
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

@bp.route('/reportar_problema/<string:id>', methods=('POST',))
#@login_required
def reportar_problema(id):
    #user_id = session.get('user_id')
    connDB = db.get_db()
    cur = connDB.cursor()

    try:
        # Incrementar el contador de status
        cur.execute("UPDATE usuario SET status = status + 1 WHERE id_usuario = %s", (id,))
        connDB.commit()
        flash('Reporte enviado. Se está investigando el problema.')
    except Exception as e:
        print(e)
        flash('Ocurrió un error al procesar el reporte. Intenta de nuevo más tarde.')
    finally:
        cur.close()
        db.close_db()

    return redirect(url_for('index'))