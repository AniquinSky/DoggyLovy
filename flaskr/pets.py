from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
from psycopg2 import Binary as to_binary

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
                    (nombre, edad, especie, raza, condicionMedica, descripcion, to_binary(foto.read()), g.user_id, paraMatch),
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
