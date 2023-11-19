from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
##from psycopg2 import Binary as to_binary

bp = Blueprint('profile', __name__, url_prefix='/site')

@bp.route('/profile', methods=('GET', 'POST'))
def myProfile():
    return render_template('site/profile.html', posts="")