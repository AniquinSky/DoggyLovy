from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db

bp = Blueprint('update_pets', __name__, url_prefix='/update_pets')

@bp.route('/update_pets/<int:id>', methods=('GET', 'POST'))
def update_pets(id):
    connDB = db.get_db()
    cur = connDB.cursor()

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        condicion_medica = request.form['condicionMedica']
        edad = request.form['edad']
        
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

        return redirect(url_for('profile.myProfile'))

    else:
        cur.execute("SELECT condicion_medica, edad, descripcion FROM mascota WHERE id_mascota = %s", (id,))
        pet_data = cur.fetchone()
        cur.close()
        db.close_db()

        if pet_data:
            return render_template('pets/update_pets.html', pet_data=pet_data)
        else:
            flash('Mascota no encontrada', 'error')
            return redirect(url_for('profile.myProfile'))