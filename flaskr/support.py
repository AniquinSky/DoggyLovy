from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
import base64

bp = Blueprint('support', __name__, url_prefix='/site')

@bp.route('/support', methods=('GET', 'POST'))
def support():
    return render_template('site/support.html')