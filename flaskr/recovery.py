from flask import (
    Blueprint, render_template, request, url_for, flash, redirect
)
import yagmail
import flaskr.db as db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('recovery', __name__, url_prefix='/recovery')

@bp.route('/recovery', methods=('GET', 'POST'))
def recovery():
    if request.method == 'POST':
        email_or_username = request.form['email']

        connDB = db.get_db()
        cur = connDB.cursor()

        cur.execute('SELECT * FROM usuario WHERE correo = %s OR id_usuario = %s', (email_or_username, email_or_username))
        user = cur.fetchone()
        cur.close()
        db.close_db()
        if user:
            print(user)
            recoveryEmail(user[2], user[0])
            flash('Se ha enviado un correo electrónico con instrucciones de recuperación.')
            return redirect(url_for('auth.login'))
        else:
            flash('No se encontró ninguna cuenta asociada a este correo electrónico o usuario.')
    #print("Entré a recovery")
    return render_template('recovery/recovery.html')
    
def recoveryEmail(email, username):
    passToken = 'skhxvywqburocwjv'
    emailPage = 'doggylovy.contact@gmail.com'
    
    yag = yagmail.SMTP(user=emailPage, password=passToken)
    
    asunto = 'Recuperación de Cuenta'
    mensaje = f'Hola {username}, haz solicitado la recuperación de tu cuenta. Haz clic en el siguiente enlace para restablecer tu contraseña: http://127.0.0.1:5000/recovery/reset_password/{username}'
    
    yag.send(email, asunto, mensaje)
    yag.close()

@bp.route('/reset_password/<string:id>', methods=('GET', 'POST'))
def reset_password(id):
    if request.method == 'POST':
        #usuario = request.form['id_usuario']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Las contraseñas no coinciden. Intenta nuevamente.', 'error')
        else:
            connDB = db.get_db()
            cur = connDB.cursor()

            cur.execute("UPDATE usuario SET password = %s WHERE id_usuario = %s",
                (generate_password_hash(new_password), id))
            connDB.commit()
            flash('Contraseña restablecida con éxito. Por favor, inicia sesión con tu nueva contraseña.')
            cur.close()
            db.close_db()
            return redirect(url_for('index'))

    return render_template('recovery/reset_password.html', id_usuario = id)
