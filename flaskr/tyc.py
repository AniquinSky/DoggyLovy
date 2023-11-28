from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
import base64

bp = Blueprint('tyc', __name__, url_prefix='/site')

@bp.route('/tyc', methods=('GET', 'POST'))
def tyc():
    return render_template('site/tyc.html')