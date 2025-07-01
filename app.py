from flask import Flask, render_template, request, redirect
import sqlite3, os

app = Flask(__name__)
DB = 'patients.db'

@app.route('/')
def home():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)