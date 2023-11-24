from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.profile import getUserPets, getUserAmountOfPetsForMatch
from flaskr.pets import getPetsForMatch

bp = Blueprint('match', __name__, url_prefix='/match')

@bp.route('', methods=('GET', 'POST'))
def match():
    if request.method == 'POST':
        pass

    # Cuando el usuario ya tiene una mascota seleccianada para el match
    if session.get('current_pet_id') is not None:
        return render_template('match/match.html', pets = getPetsForMatch())

    amount_of_pets = getUserAmountOfPetsForMatch()
    # Si solo tiene una se manda al usuario directo al match
    if amount_of_pets == 1:
        session['current_pet_id'] = getUserPets()[0]
        return render_template('match/match.html', pets = getPetsForMatch())
    # Si tiene mas de una, selecciona la mascota para el match
    elif amount_of_pets > 1:
        return render_template('match/select_pet_for_match.html', pets = getUserPets())
    # Si no tiene mascotas registradas se redirige al registro de mascotas
    elif amount_of_pets == 0:
        flash('Antes de acceder al match debe registrar una mascota.')
        return render_template('pets/register_pets.html')
    else:
        flash('Ocurrio un erros inesperado. Intentelo de nuevo mas tarde.')
        return render_template('site/home.html')

    return render_template('site/home.html')

@bp.route('/selectPet/<int:petId><petName>')
def petSelected(petId, petName):
    session['current_pet_id'] = petId
    session['current_pet_name'] = petName
    return redirect(url_for('pets.match.match'))
