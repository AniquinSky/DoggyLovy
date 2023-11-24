from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
from psycopg2 import Binary as to_binary
import base64

bp = Blueprint('pets', __name__, url_prefix='/pets')

@bp.route('/registerPets', methods=('GET', 'POST'))
def registerPets():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        especie = request.form['especie']
        raza = request.form['raza']
        condicionMedica = request.form['condicionMedica']
        descripcion = request.form['descripcion']
        foto = request.files['foto_mascota']
        destino = request.form['destino']

        error = None

        if not nombre:
            error = 'Nombre de mascota necesario.'
        if not edad:
            error = 'Edad de mascota necesaria.'
        if not especie:
            error = 'Especie de mascota necesaria.'
        if not raza:
            error = 'Raza de mascota necesaria.'
        if not condicionMedica:
            error = 'Condicion medica necesaria.'
        if not descripcion:
            error = 'descripcion de mascota necesara.'
        if not foto:
            error = 'Foto de mascota necesaria.'
        if not destino:
            error = 'Seleccion de match o adopcion necesaria.'

        if error is None:
            fotoData = foto.read()
            paraMatch = True if destino == 'match' else False
            connDB = db.get_db()
            cur = connDB.cursor()
            try:
                cur.execute(
                    "INSERT INTO mascota VALUES (default, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (nombre, edad, especie, raza, condicionMedica, descripcion, to_binary(fotoData), g.user_id, paraMatch),
                )
                connDB.commit()
            except Exception as e:
                print(e)
                error = "Ocurrio un error inesperado. Intentelo mas tarde."
            cur.close()
            db.close_db()

            if error is None:
                return redirect(url_for("index"))

        flash(error)

    return render_template('pets/register_pets.html')

@bp.route('/deletePet/<int:petId>')
def deletePet(petId):
    connDB = db.get_db()
    cur = connDB.cursor()

    try:
        cur.execute('DELETE FROM mascota WHERE id_mascota=%s', (petId,))
        connDB.commit()
        session.pop('current_pet_id')
        session.pop('current_pet_name')
        flash('Mascota eliminada con exito.')
    except Exception as e:
        print(e)
        flash('Ocurrio un error. Intentelo de nuevo mas tarde.')
    finally:
        cur.close()
        db.close_db()

    return redirect(url_for('profile.myProfile'))

def getPetsForAdoption():
    """Get pets for adoption
    If error occurs return None.

    Otherwise return array of tuples composed of:
    [0] id_mascota
    [1] nom_mascota
    [3] edad,
    [4] raza,
    [5] condicion_medica,
    [6] descripcion,
    [7] imagen, ready for render it in html with data:image/jpg;base64
    [8] id_dueno
    [9] para_match
    [10] likes,
    [11] dislikes,
    """
    connDB = db.get_db()
    cur = connDB.cursor()
    pets = []
    try:
        cur.execute(
            'SELECT * FROM mascota WHERE para_match=FALSE AND id_dueno!=%s',
            (g.user_id,)
        )
        results = cur.fetchall()
        for record in results:
            image_in_base64 = base64.b64encode(record[7]).decode('utf-8')
            pets.append((record[0], record[1], record[2], record[3], record[4], record[5], record[6], image_in_base64, record[8], record[9], record[10], record[11]))
    except Exception as e:
        print(e)
        pets = None
    finally:
        cur.close()
        db.close_db()

    return pets

def getPetsForMatch():
    """Get pets for adoption
    If error occurs return None.

    Otherwise return array of tuples composed of:
    [0] id_mascota
    [1] nom_mascota
    [3] edad,
    [4] raza,
    [5] condicion_medica,
    [6] descripcion,
    [7] imagen, ready for render it in html with data:image/jpg;base64
    [8] id_dueno
    [9] para_match
    [10] likes,
    [11] dislikes,
    """
    connDB = db.get_db()
    cur = connDB.cursor()
    pets = []
    try:
        cur.execute('SELECT * FROM mascota WHERE para_match=TRUE AND id_dueno != %s', (g.user_id,))
        results = cur.fetchall()
        for record in results:
            image_in_base64 = base64.b64encode(record[7]).decode('utf-8')
            pets.append((record[0], record[1], record[2], record[3], record[4], record[5], record[6], image_in_base64, record[8], record[9], record[10], record[11]))
    except Exception as e:
        print(e)
        pets = None
    finally:
        cur.close()
        db.close_db()

    return pets

@bp.route('/like/<int:id>', methods=['POST'])
def like_pet(id):
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute('UPDATE mascota SET likes = likes + 1 WHERE id_mascota = %s', (id,))
        flash('Has dado like', 'success')
        connDB.commit()
    except Exception as e:
        print(e)
        connDB.rollback()
    finally:
        cur.close()
        db.close_db()
    return redirect(url_for('profile.myProfile'))

@bp.route('/dislike/<int:id>', methods=['POST'])
def dislike_pet(id):
    connDB = db.get_db()
    cur = connDB.cursor()
    try:
        cur.execute('UPDATE mascota SET dislikes = dislikes + 1 WHERE id_mascota = %s', (id,))
        flash('Has dado dsilike', 'success')
        connDB.commit()
    except Exception as e:
        print(e)
        connDB.rollback()
    finally:
        cur.close()
        db.close_db()
    return redirect(url_for('profile.myProfile'))