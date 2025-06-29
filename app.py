from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB = os.path.join('/tmp', 'data.db')

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT)')
init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    items = conn.execute('SELECT * FROM items').fetchall()
    conn.close()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    conn = sqlite3.connect(DB)
    conn.execute('INSERT INTO items (name) VALUES (?)', (name,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect(DB)
    if request.method == 'POST':
        name = request.form['name']
        conn.execute('UPDATE items SET name=? WHERE id=?', (name, id))
        conn.commit()
        return redirect(url_for('index'))
    item = conn.execute('SELECT * FROM items WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect(DB)
    conn.execute('DELETE FROM items WHERE id=?', (id,))
    conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)