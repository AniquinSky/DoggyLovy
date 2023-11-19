from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
##from psycopg2 import Binary as to_binary

bp = Blueprint('adoption', __name__, url_prefix='/site')

@bp.route('/adoption', methods=('GET', 'POST'))
def adoption():
    return render_template('site/adoption.html', posts="")