from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from flaskr.profile import getUserPets, getUserAmountOfPetsForMatch

bp = Blueprint('match', __name__, url_prefix='/match')

@bp.route('', methods=('GET', 'POST'))
def match():
    if request.method == 'POST':
        pass

    if session.get('current_pet_id') is not None:
        return render_template('match/match.html')

    amount_of_pets = getUserAmountOfPetsForMatch()
    if amount_of_pets == 1:
        session['current_pet_id'] = getUserPets()[0]
        return render_template('match/match.html')
    elif amount_of_pets > 1: #Para que el usuario seleccione a la mascota para acceder al match
        return render_template('match/select_pet_for_match.html', pets = getUserPets())
    elif amount_of_pets == 0:
        # Poner mensaje que tiene que registrar por lo menos una mascota
        return render_template('site/home.html')
    else:
        flash('Ocurrio un erros inesperador. Intentelo de nuevo mas tarde.')
        return render_template('site/home.html')

    return render_template('site/home.html')

@bp.route('/selectPet/<int:petId><petName>')
def petSelected(petId, petName):
    session['current_pet_id'] = petId
    session['current_pet_name'] = petName
    print('ID', petId)
    print('Name', petName)
    return redirect(url_for('pets.match.match'))
