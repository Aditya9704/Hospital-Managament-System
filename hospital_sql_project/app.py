from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="root",  # change to your MySQL password
        database="hospital"
    )

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['age'],
            request.form['gender'],
            request.form['contact'],
            request.form['address'],
            request.form['disease'],
            request.form['doctor'],
            request.form['status']
        )
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO patients (name, age, gender, contact, address, disease, doctor, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', data)
        conn.commit()
        conn.close()
        return redirect('/view')
    return render_template("add_patient.html")

@app.route('/view')
def view_patients():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    rows = cur.fetchall()
    conn.close()
    return render_template("view_patients.html", patients=rows)

if __name__ == '__main__':
    app.run(debug=True)
