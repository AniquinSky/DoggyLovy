from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
from psycopg2 import Binary as to_binary

bp = Blueprint('pets', __name__, url_prefix='/pets')

@bp.route('/registerPets', methods=('GET', 'POST'))
def registerPets():
    if request.method == 'POST':
        # Logica registro de mascota
        pass

    return render_template('pets/register_pets.html')
