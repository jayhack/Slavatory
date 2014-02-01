# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, abort, \
     render_template, flash


#==========[ Create the application ]
app = Flask(__name__)

# Load default config and override config from an environment variable

#==========[ Load default config and override config from an enviornment variable ]==========
app.config.update(dict(
    DATABASE='/tmp/slavatory.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# Function: connect_db
# --------------------
# connects to the specific databse
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# Function: init_db
# -----------------
# initializes the database
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# Function: get_db
# ----------------
# Opens a new database connection if there is none yet for the
# current application context.
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        print g.sqlite_db
    return g.sqlite_db


# Function: close_db
# ------------------
# Closes the database again at the end of the request.
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# Function: show_entries
# ----------------------
# shows all entries from the blog
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select text from entries_test order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


# Function: add_entry
# -------------------
# allows you to add an entry
@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    db.execute('insert into entries_test (text, painting_id) values (?, ?)', [request.form['text'], request.form['painting_id']])
    db.commit()
    return redirect(url_for('show_entries'))



if __name__ == '__main__':
    init_db()
    app.run()
