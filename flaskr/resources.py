import functools

from flask import (
    Blueprint, flash, g, Flask, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('resources', __name__)

@bp.route('/resources')
def resources():
    return render_template('resources.html')