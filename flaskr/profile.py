from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
import base64
##from psycopg2 import Binary as to_binary

bp = Blueprint('profile', __name__, url_prefix='/site')

@bp.route('/profile', methods=('GET', 'POST'))
def myProfile():
    return render_template('site/profile.html', posts="")

def getInfoForProfilePage():
    profile_picture = None
    pets = []

    connDB = db.get_db()
    cur = connDB.cursor()

    # obtener imagen de perfil del usuario
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

    connDB = db.get_db()
    cur = connDB.cursor()
    # obtener mascotas del usuario
    try:
        cur.execute('SELECT nom_mascota, imagen, raza FROM mascota WHERE id_dueno=%s', (g.user_id,))
        results = cur.fetchall()
        for record in results:
            image_in_base64 = base64.b64encode(record[1]).decode('utf-8')
            pets.append((record[0], image_in_base64, record[2]))
    except Exception as e:
        print(e)
        pets = None
    finally:
        cur.close()
        db.close_db()

    return (profile_picture, pets)
