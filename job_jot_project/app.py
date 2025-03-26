
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'jobs.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            applied_on TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM jobs")
    jobs = c.fetchall()
    conn.close()
    return render_template('index.html', jobs=jobs)

@app.route('/add', methods=['GET', 'POST'])
def add_job():
    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        applied_on = request.form['applied_on']
        status = request.form['status']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("INSERT INTO jobs (company, role, applied_on, status) VALUES (?, ?, ?, ?)",
                  (company, role, applied_on, status))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if request.method == 'POST':
        company = request.form['company']
        role = request.form['role']
        applied_on = request.form['applied_on']
        status = request.form['status']
        c.execute("UPDATE jobs SET company=?, role=?, applied_on=?, status=? WHERE id=?",
                  (company, role, applied_on, status, job_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        c.execute("SELECT * FROM jobs WHERE id=?", (job_id,))
        job = c.fetchone()
        conn.close()
        return render_template('edit.html', job=job)

@app.route('/delete/<int:job_id>')
def delete_job(job_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM jobs WHERE id=?", (job_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
