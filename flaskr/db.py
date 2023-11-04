#import sqlite3
#import click
import psycopg2

from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
        host="dpg-ckhis1q12bvs73eifn20-a.oregon-postgres.render.com",
        database="dbdl",
        user="dbdl_user",
        password="7cBb7xPj2caB9DUbJDJeAyVXwEXAi6VW")
#        g.db = sqlite3.connect(
#            current_app.config['DATABASE'],
#            detect_types=sqlite3.PARSE_DECLTYPES
#        )
#        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#def init_db():
#    db = get_db()
#
#    with current_app.open_resource('schema.sql') as f:
#        db.executescript(f.read().decode('utf8'))
#
#@click.command('init-db')
#def init_db_command():
#    """Clear the existing data and create new tables."""
#    init_db()
#    click.echo('Initialized the database.')
#
#def init_app(app):
#    app.teardown_appcontext(close_db)
#    app.cli.add_command(init_db_command)