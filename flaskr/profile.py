from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('profile', __name__)

@bp.route('/profile')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('profile.html', posts=posts)

def get_document(id, check_author=True):
    document = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM document p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if document is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and document['author_id'] != g.user['id']:
        abort(403)

    return document

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    document = get_document(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('update.html', post=document)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_document(id)
    db = get_db()
    db.execute('DELETE FROM document WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('profile'))