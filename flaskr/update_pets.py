from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
from flaskr.profile import getUserPets

bp = Blueprint('update_pets', __name__, url_prefix='/update_pets')

@bp.route('/update_pets/<int:id>', methods=('GET', 'POST'))
def update_pets(id):
    if request.method == 'POST':
        print(request.form)
        descripcion = request.form['descripcion']
        condicion_medica = request.form['condicionMedica']
        edad = request.form['edad']
        
        connDB = db.get_db()
        cur = connDB.cursor()
        try:
            cur.execute(
                "UPDATE mascota SET condicion_medica = %s, edad = %s, descripcion = %s WHERE id_mascota = %s",
                (condicion_medica, edad, descripcion, id)
            )
            connDB.commit()
            flash('Datos de mascota actualizados con éxito', 'success')
        except connDB.IntegrityError as e:
            error = "Datos faltantes."
            print(e)
            flash('Error: Datos faltantes', 'error')
        except Exception as e:
            print(e)
            error = "Ocurrió un error inesperado. Inténtelo más tarde."
            flash('Error: Ocurrió un error inesperado', 'error')
        finally:
            cur.close()
            db.close_db()

        return render_template('site/profile.html', pets = getUserPets())

    return render_template('pets/update_pets.html')
