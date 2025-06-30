
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = 'patients.db'

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        phone = request.form['phone']
        insurance = request.form['insurance']
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute("INSERT INTO patients (name, gender, dob, phone, insurance) VALUES (?, ?, ?, ?, ?)",
                    (name, gender, dob, phone, insurance))
        conn.commit()
        conn.close()
        return redirect('/patients')
    return render_template('register.html')

@app.route('/patients')
def patient_list():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    patients = cur.fetchall()
    conn.close()
    return render_template('patients.html', patients=patients)

@app.route('/consult/<int:patient_id>', methods=['GET', 'POST'])
def consult(patient_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    if request.method == 'POST':
        complaints = request.form['complaints']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        cur.execute("INSERT INTO consultations (patient_id, complaints, diagnosis, treatment) VALUES (?, ?, ?, ?)",
                    (patient_id, complaints, diagnosis, treatment))
        conn.commit()
        conn.close()
        return redirect('/patients')
    cur.execute("SELECT name FROM patients WHERE id = ?", (patient_id,))
    patient = cur.fetchone()
    conn.close()
    return render_template('consult.html', patient_id=patient_id, patient_name=patient[0])

if __name__ == '__main__':
    app.run()
