from flask import Flask, render_template, request
import sqlite3
import numpy as np
import pickle

app = Flask(__name__)

# Load trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Home page: form input
@app.route('/')
def index():
    return render_template('index.html')

# Predict route
@app.route('/predict', methods=['POST'])
def predict():
    name = request.form['name']
    hours = float(request.form['hours'])
    attendance = float(request.form['attendance'])

    # Custom logic: chance if hours are high
    if hours < 4 and attendance < 50:
        prediction_result = 0  # Fail
    else:
        features = np.array([[hours, attendance]])
        prediction_result = model.predict(features)[0]

    status = "PASS" if prediction_result == 1 else "FAIL"

    # Save to DB
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            hours REAL,
            attendance REAL,
            status TEXT
        )
    ''')
    c.execute("INSERT INTO students (name, hours, attendance, status) VALUES (?, ?, ?, ?)",
              (name, hours, attendance, status))
    conn.commit()
    conn.close()

    return render_template("result.html", result=f"{name}: {'✅ PASS' if status == 'PASS' else '❌ FAIL'}")

# View all students
@app.route('/students')
def show_students():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template("students.html", students=students)

if __name__ == '__main__':
    app.run(debug=True)
