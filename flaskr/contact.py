from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

import flaskr.db as db
import base64

bp = Blueprint('contact', __name__, url_prefix='/site')

@bp.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('site/contact.html')