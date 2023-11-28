from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
import base64

bp = Blueprint('service', __name__, url_prefix='/site')

@bp.route('/service', methods=('GET', 'POST'))
def service():
    return render_template('site/service.html')