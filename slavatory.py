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
@app.route('/', methods=['GET'])
def show_entries():

    #==========[ Step 1: establish connection w/ database ]==========
    db = get_db()

    #==========[ Step 2: get image data ]==========
    image_id    = request.args.get ('image_id')
    if not image_id:
        image_id = 1
    cur         = db.execute ('select url, artist, description from images where id = (?)', [image_id])
    entries     = cur.fetchall ()
    url         = entries[0][0]
    artist      = entries[0][1]
    description = entries[0][2]

    print "==========[ IMAGE INFO ]=========="
    print "image id: ", image_id
    print "url: ", url
    print "artist: ", artist
    print "description: ", description

    #==========[ Step 3: get associated comments from db ]==========
    cur         = db.execute('select text from comments where image_id = (?) order by id asc', [image_id])
    entries     = cur.fetchall()
    comments    = [e[0] for e in entries]
    print "==========[ ASSOCIATED COMMENTS ]=========="
    print comments
    print "\n\n"
    return render_template('show_entries.html', entries=entries, image_id=image_id)



# Function: add_entry
# -------------------
# allows you to add an entry
@app.route('/add', methods=['POST'])
def add_entry():
    db = get_db()
    print "==========[ ADD ENTRY ]=========="
    print request.form
    print "\n\n"
    db.execute('insert into comments (text, image_id) values (?, ?)', [request.form['text'], request.form['imageID']])
    db.commit()
    return redirect(url_for('show_entries') + '/?image_id=' + str(request.form['imageID']))


# Function: add_image
# -------------------
# allows you to add an image
def add_image (url, artist, description):
    db = get_db ()
    db.execute ('insert into images (url, artist, description) values (?, ?, ?)', [url, artist, description])
    db.commit ()


if __name__ == '__main__':
    # init_db ()
    app.run()
