from flask import Flask, request, render_template, redirect, url_for, jsonify
import pymysql
import pandas as pd
app = Flask(__name__)

config = {
    'user' : 'root',
    'password' : 'rlaqhdbs3586!',
    'host' : 'localhost',
    'db' : 'AppClassDB',
    'port' : 3306,
    'cursorclass' : pymysql.cursors.DictCursor
}


@app.route('/')
def home():
    return render_template('firstPage.html')

@app.route('/status')
def status():
    return render_template('sstatus.html')

@app.route('/buket')
def buket():
    return render_template('sbuket.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username)
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM logintable WHERE id=%s AND pwd=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            print("login successed")
            return redirect(url_for('home'))
        else:
            return render_template('slogin.html', login_failed=True)
    return render_template('slogin.html')


if __name__ == '__main__':
    app.run(debug=True)


