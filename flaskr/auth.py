import functools

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
        password = request.form['password']
        correo = request.form['correo']

        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            connDB = db.get_db()
            cur = connDB.cursor()
            try:
                cur.execute(
                    "INSERT INTO usuario (id_usuario, password, correo) VALUES (%s, %s, %s)",
                    (username, generate_password_hash(password), correo),
                )
                connDB.commit()
            except connDB.IntegrityError:
                error = f"User {username} is already registered."
            cur.close()
            db.close_db()
        else:
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
            'SELECT id_usuario, password FROM usuario WHERE id_usuario = %s', (username,)
        )
        user = cur.fetchone()
        cur.close()
        db.close_db()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[1], password):
            error = 'Incorrect password.'

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