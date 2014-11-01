# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2014 by Armin Ronacher.
    :copyright: (c) 2014 by Niclas Moeslund Overby.
    :license: BSD, see LICENSE for more details.
"""

from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__)

app.config.update(dict(
    DATABASE='/tmp/flaskr.db',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('menu.html')

@app.route('/order', methods=['GET', 'POST'])
def order():
    db = get_db()
    cur = db.execute('select Id, Title, Text from Products order by Id asc')
    products = cur.fetchall()
    return render_template('order.html', products=products)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    #print(int(request.form["order"]))
    db = get_db()
    db.execute('insert into Orders (Client,P_Id) values (?, ?)',
                 [request.form['client'], int(request.form["order"])])
    db.commit()
    flash('Din bestilling var succesfuld!')
    
    return redirect(url_for('queue'))

@app.route('/product', methods=['GET', 'POST'])
def product():
    return render_template('product.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    db = get_db()
    db.execute('insert into Products (Title, Text , Stat1, Stat2, Stat3) values (?, ?, ?, ?, ?)',
                 [request.form['title'], request.form['text'],request.form['stat1'],request.form['stat2'],request.form['stat3']])
    db.commit()
    flash(u'Produktet blev tilføjet')
    return redirect(url_for('root'))

@app.route('/queue', methods=['GET', 'POST'])
def queue():
    db = get_db()
    cur = db.execute('select Id, P_Id, Client from Orders order by Id asc')
    orders = cur.fetchall()
    cur = db.execute('select Id, Title from Products order by Id asc')
    products = cur.fetchall()
    return render_template('queue.html', orders=orders, products=products)

@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_orders'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    init_db()
    app.run()
