# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, g, redirect, url_for, abort, \
     render_template, flash
import sys


########################################################################################################################
##############################[ --- App Configuration --- ]#############################################################
########################################################################################################################

app = Flask(__name__)
app.config.update(dict(
    DATABASE='/tmp/slavatory.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)










########################################################################################################################
##############################[ --- Database Management --- ]###########################################################
########################################################################################################################

def init_db (app):
    """
        Function: init_db
        -----------------
        initializes the database w/ settings described in
        schema.sql
    """
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    """
        Function: connect_db
        --------------------
        connects to database
    """
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """
        Function: get_db
        ----------------
        Opens a new database connection if there is none yet for the
        current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        print g.sqlite_db
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """
        Function: close_db
        ------------------
        Closes the database at the end of the request.
    """
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()










########################################################################################################################
##############################[ --- Viewing/Comenting on Images --- ]###################################################
########################################################################################################################

@app.route('/', methods=['GET'])
def show_entries():
    """
        Function: show_entries
        ----------------------
        serves up landing page for once you scan the QR code.
        there should be images in the database when you call this.
        called with ?image_id=XXX
    """

    #==========[ Step 1: establish connection w/ database ]==========
    db = get_db()
    # db.execute ('insert into images (url, artist, description) values (?, ?, ?)', ['test_url', 'test_artist', 'test_description'])
    # db.execute ('insert into images (url, artist, description) values (?, ?, ?)', ['test_url_2', 'test_artist_2', 'test_description_2'])    
    # db.commit ()

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
    return render_template('index.html', entries=entries, image_id=image_id, image_url=url)


@app.route('/add', methods=['POST'])
def add_entry():
    """
        Funtion: add_entry
        ------------------
        adds a comment to the specified image
    """
    db = get_db()
    print "==========[ ADD ENTRY ]=========="
    print request.form
    print "\n\n"
    db.execute('insert into comments (text, image_id) values (?, ?)', [request.form['text'], request.form['imageID']])
    db.commit()
    return redirect(url_for('show_entries') + '/?image_id=' + str(request.form['imageID']))










########################################################################################################################
##############################[ --- Adding Images --- ]#################################################################
########################################################################################################################

@app.route ('/add_image', methods=['GET'])
def add_image ():
    """
        Function: add_image
        -------------------
        function for adding an image
    """
    
    url = request.args.get('url')
    artist = request.args.get('artist')
    description = request.args.get('description')
    print "artist: ", artist
    print "url: ", url
    print "Description: ", description
    return redirect(url_for('show_entries') + '/?image_id=0')


def put_in_image (url, artist, description):
    """
        Function: put_in_image
        ----------------------
        adds the image described by url, artist and description
        into the database 
    """
    db = get_db ()
    db.execute ('insert into images (url, artist, description) values (?, ?, ?)', [url, artist, description])
    db.commit ()








########################################################################################################################
##############################[ --- Main Operation --- ]################################################################
########################################################################################################################


if __name__ == '__main__':

    #=====[ Mode: database initialization ]=====
    if len(sys.argv) == 2:
        if sys.argc[1] == 'init_db':
            init_db (app)
            exit ()


    #=====[ Mode: regular operation  ]=====
    else:
        app.run()
