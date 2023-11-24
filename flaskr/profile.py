from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
import base64

bp = Blueprint('profile', __name__, url_prefix='/site')

@bp.route('/profile', methods=('GET', 'POST'))
def myProfile():
    return render_template('site/profile.html', pets = getUserPets(), fotoPerfil = getUserProfilePicture())

def getUserProfilePicture():
    """Get user's profile picture
    If error occurs return None.
    Otherwise returns Profile Picture ready for render it in html with data:image/jpe;base64
    """
    profile_picture = None

    connDB = db.get_db()
    cur = connDB.cursor()

    try:
        cur.execute('SELECT profile_pic FROM usuario WHERE id_usuario=%s', (g.user_id,))
        profile_picture = cur.fetchone()
        profile_picture = base64.b64encode(profile_picture[0]).decode('utf-8')
    except Exception as e:
        print(e)
        profile_picture = None
    finally:
        cur.close()
        db.close_db()

    return profile_picture

def getUserPets():
    """Get user's pets
    If error occurs returns None.

    Otherwise returns array of tuples composed of:
    [0] id_mascota
    [1] nom_mascota
    [2] imagen, ready for render it in html with data:image/jpg;base64
    [3] raza,
    [4] para_match
    """
    pets = []

    connDB = db.get_db()
    cur = connDB.cursor()

    try:
        cur.execute('SELECT id_mascota, nom_mascota, imagen, raza, para_match FROM mascota WHERE id_dueno=%s', (g.user_id,))
        results = cur.fetchall()
        for record in results:
            image_in_base64 = base64.b64encode(record[2]).decode('utf-8')
            pets.append((record[0], record[1], image_in_base64, record[3], record[4]))
    except Exception as e:
        print(e)
        pets = None
    finally:
        cur.close()
        db.close_db()

    return pets

def getUserAmountOfPetsForMatch():
    amount = 0
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute('SELECT COUNT(nom_mascota) FROM mascota WHERE id_dueno = %s AND para_match=TRUE', (g.user_id,))
        amount = cur.fetchone()[0]
    except Exception as e:
        print(e)
        amount = -1
    finally:
        cur.close()
        db.close_db()

    return amount

@bp.route('/like/<string:user_id>', methods=['POST'])
def like_user(user_id):
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute('UPDATE usuario SET likes = likes + 1 WHERE id_usuario = %s', (user_id,))
        flash('Has dado like', 'success')
        connDB.commit()
    except Exception as e:
        print(e)
        connDB.rollback()
    finally:
        cur.close()
        db.close_db()
    return redirect(url_for('profile.myProfile'))

@bp.route('/dislike/<string:user_id>', methods=['POST'])
def dislike_user(user_id):
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute('UPDATE usuario SET dislikes = dislikes + 1 WHERE id_usuario = %s', (user_id,))
        flash('Has dado dsilike', 'success')
        connDB.commit()
    except Exception as e:
        print(e)
        connDB.rollback()
    finally:
        cur.close()
        db.close_db()
    return redirect(url_for('profile.myProfile'))