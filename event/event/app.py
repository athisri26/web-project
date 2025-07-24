from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import pymysql
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Athi@2627',
    'database': 'event',
    'cursorclass': pymysql.cursors.DictCursor
}
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
            admin = cur.fetchone()
        conn.close()
        if admin:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

# Admin Dashboard
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM events")
        events = cur.fetchall()
    conn.close()
    return render_template('admin_dashboard.html', events=events)

# Add Event
@app.route('/admin/add', methods=['GET', 'POST'])
def add_event():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        event_name = request.form['event_name']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        description = request.form['description']
        chief_guest = request.form['chief_guest']
        image = request.files.get('image')
        filename = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO events (event_name, start_time, end_time, image, description, chief_guest) VALUES (%s, %s, %s, %s, %s, %s)",
                        (event_name, start_time, end_time, filename, description, chief_guest))
        conn.commit()
        conn.close()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_event.html')

# Edit Event
@app.route('/admin/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    with conn.cursor() as cur:
        if request.method == 'POST':
            event_name = request.form['event_name']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            description = request.form['description']
            chief_guest = request.form['chief_guest']
            image = request.files.get('image')
            filename = None
            if image and image.filename:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                cur.execute("UPDATE events SET event_name=%s, start_time=%s, end_time=%s, image=%s, description=%s, chief_guest=%s WHERE event_id=%s",
                            (event_name, start_time, end_time, filename, description, chief_guest, event_id))
            else:
                cur.execute("UPDATE events SET event_name=%s, start_time=%s, end_time=%s, description=%s, chief_guest=%s WHERE event_id=%s",
                            (event_name, start_time, end_time, description, chief_guest, event_id))
            conn.commit()
            conn.close()
            return redirect(url_for('admin_dashboard'))
        else:
            cur.execute("SELECT * FROM events WHERE event_id=%s", (event_id,))
            event = cur.fetchone()
    conn.close()
    return render_template('edit_event.html', event=event)

# Delete Event
@app.route('/admin/delete/<int:event_id>')
def delete_event(event_id):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM events WHERE event_id=%s", (event_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

# User: Homepage
@app.route('/')
def home():
    return render_template('home.html')

# User: View All Events
@app.route('/events')
def events():
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM events")
        events = cur.fetchall()
    conn.close()
    return render_template('events.html', events=events)

# User: View Event Details
@app.route('/event/<int:event_id>')
def event_detail(event_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM events WHERE event_id=%s", (event_id,))
        event = cur.fetchone()
    conn.close()
    return render_template('event_detail.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)
