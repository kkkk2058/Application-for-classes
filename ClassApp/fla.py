# from flask import Flask, render_template, request, redirect, url_for, session, flash
# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField
# from wtforms.validators import DataRequired
# import mysql.connector

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Change this to a random secret key

# def get_db_connection():
#     conn = mysql.connector.connect(
#         user='adm_1', password='ssu_serverprog', host='10.29.112.30', database='AppClassDB', port='3306'
#     )
#     return conn

# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired()])
#     password = PasswordField('Password', validators=[DataRequired()])

# @app.route('/', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         username = form.username.data
#         password = form.password.data
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM logintable WHERE username = %s AND password = %s", (username, password))
#         account = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         if account:
#             session['logged_in'] = True
#             return redirect(url_for('home'))
#         else:
#             flash('Invalid username or password')
#     return render_template('login.html', form=form)

# @app.route('/home')
# def home():
#     if not session.get('logged_in'):
#         return redirect(url_for('login'))
#     return 'Logged in successfully!'

# if __name__ == '__main__':
#     app.run(debug=True)
