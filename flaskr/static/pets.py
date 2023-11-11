bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/registerPets', methods=('GET', 'POST'))
def registerPets():
    if request.method == 'POST':

    return render_template('auth/register_pets.html')
