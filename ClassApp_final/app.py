from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import pymysql
import pandas as pd
import mpld3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy
from data_proc import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'
config = {
    'user' : 'root',
    'password' : 'rpg112119@',
    'host' : 'localhost',
    'db' : 'AppClassDB',
    'port' : 3306,
    'cursorclass' : pymysql.cursors.DictCursor
}



@app.route('/')
def home():
    if 'user_info' in session:
        user_info = session['user_info']
        # grade = user_info['grade']
        
        conn = pymysql.connect(**config)
        try:
            cursor = conn.cursor()
            
            sbj_id = session.get('sbj_id')
            
            if sbj_id:
                cursor.execute("SELECT ave_score, assignment_amt, test_difficulty, lecture_session, projects_amt FROM subInfoTable WHERE sbj_id=%s", (sbj_id,))
                result = cursor.fetchone()
                
                if result:
                    scores = list(result.values())
                else:
                    scores = [0, 0, 0, 0, 0]
            else:
                scores = [1, 0, 0, 0, 0]
            
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            scores = [0, 1, 0, 0, 0]
        finally:
            cursor.close()
            conn.close()
        
        return render_template('firstPage.html', user_info = user_info, scores=scores)
    else:
        return redirect(url_for('login'))

@app.route('/cartvis', methods=['GET', 'POST'])
def cartvis():
    if 'user_info' in session:
        user_info = session['user_info']
        return render_template('cartvis.html', user_info=user_info)
    return render_template('slogin.html')

@app.route('/cartvis/get_vis_html')
def get_vis_html():
    if 'user_info' in session:
        user_info = session['user_info']
    else:
        return redirect(url_for('login'))
    
    conn = pymysql.connect(**config)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subinfotable")
        subinfotable = cursor.fetchall()
        cursor.execute("SELECT * FROM carttable")
        carttable = cursor.fetchall()
        cursor.execute("SELECT * FROM logintable")
        logintable = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return jsonify([])  # Return an empty list if there is an error
    finally:
        cursor.close()
        conn.close()
    
    user_id = user_info['id']
    priority = request.args.get('priority', default=1, type=int)
    
    graphvis_html = get_visdata(subinfotable, carttable, logintable, user_id, priority)
    return render_template('safe_vis.html', graphvis_html=graphvis_html)

@app.route('/status')
def status():
    return render_template('sstatus.html')



@app.route('/buket/get_scores')
def get_scores():
    user_info = session.get('user_info')
    if user_info:
        scores = get_subject_scores(user_info['id'])
        return jsonify(scores)
    else:
        return jsonify([])

@app.route('/buket/get_subs')
def get_subs():
    conn = pymysql.connect(**config)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subinfotable")
        subinfotable = cursor.fetchall()
        cursor.execute("SELECT * FROM carttable")
        carttable = cursor.fetchall()
        cursor.execute("SELECT * FROM logintable")
        logintable = cursor.fetchall()
        
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return jsonify([])  # Return an empty list if there is an error
    
    finally:
        cursor.close()
        conn.close()
    
    view_subs = rebuild_subs(subinfotable, carttable, logintable)
    return jsonify(view_subs)

@app.route('/buket')
def buket():
    if 'user_info' in session:
        user_info = session['user_info']
        std_id = user_info['id']
        
        conn = pymysql.connect(**config)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM carttable WHERE std_id=%s", (std_id,))
            mycart = cursor.fetchall()
            cursor.execute("SELECT * FROM subinfotable")
            subs = cursor.fetchall()
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return render_template('slogin.html')  # Redirect to login on error
        finally:
            cursor.close()
            conn.close()
        
        return render_template('sbuket.html', user_info=user_info, mycart=mycart, subs=subs)
    return render_template('slogin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = pymysql.connect(**config)
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM logintable WHERE id=%s AND pwd=%s", (username, password))
            user = cursor.fetchone()
            
            if user:
                # Correct the query to fetch sbj_id based on the user's ID from the cartTable
                cursor.execute("SELECT sbj_id FROM cartTable WHERE std_id=%s", (user['id'],))
                sbj = cursor.fetchone()
                
                session['user_info'] = user
                if sbj != None:
                    session['sbj_id'] = sbj['sbj_id'] 
                
                return redirect(url_for('home'))
            else:
                return render_template('slogin.html', login_failed=True)
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return render_template('slogin.html', login_failed=True)
        finally:
            cursor.close()
            conn.close()
    
    return render_template('slogin.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/subject/<subject_name>', methods=['GET'])
def get_subject_info(subject_name):
    conn = pymysql.connect(**config)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subinfotable WHERE subject_name=%s", (subject_name,))
        subject = cursor.fetchone()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Subject not found'}), 404
    finally:
        cursor.close()
        conn.close()

    if subject:
        subject_info = {
            'lectureRating': subject['ave_score'],
            'assignmentCount': subject['assignment_amt'],
            'examDifficulty': subject['test_difficulty'],
            'lectureTime': subject['lecture_session'],
            'studentCount': subject['projects_amt']
        }
        return jsonify(subject_info)
    else:
        return jsonify({'error': 'Subject not found'}), 404
    

@app.route('/buket/get_cart')
def get_cart():
    user_info = session.get('user_info')
    if not user_info:
        return jsonify({'error': 'User not logged in'}), 401

    std_id = user_info['id']
    
    conn = pymysql.connect(**config)
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM carttable WHERE std_id=%s", (std_id,))
        cart = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(cart)



@app.route('/buket/add', methods=['POST'])
def add_to_cart():
    if 'user_info' in session:
        user_info = session['user_info']
        std_id = user_info['id']
        sbj_id = request.json.get('sbj_id')
        priority = request.json.get('priority')

        conn = pymysql.connect(**config)
        try:
            cursor = conn.cursor()

            # Check if the subject is already in the cart
            cursor.execute("SELECT * FROM cartTable WHERE std_id=%s AND sbj_id=%s", (std_id, sbj_id))
            cart_item = cursor.fetchone()
            
            if cart_item:
                return jsonify({'error': 'Course already in cart'}), 409  # Conflict error code
            
            # Fetch the subject name from subInfoTable
            cursor.execute("SELECT subject_name FROM subInfoTable WHERE sbj_id=%s", (sbj_id,))
            result = cursor.fetchone()

            if result:
                subject_name = result['subject_name']
                cursor.execute("INSERT INTO cartTable (std_id, sbj_id, subject, priority) VALUES (%s, %s, %s, %s)", 
                               (std_id, sbj_id, subject_name, priority))
                conn.commit()
                return jsonify({'message': 'Course added to cart successfully'}), 200
            else:
                return jsonify({'error': 'Subject not found'}), 404
        except pymysql.MySQLError as e:
            print(f"Error: {e}")  # Log the error message
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'User not logged in'}), 401

    



@app.route('/buket/remove', methods=['POST'])
def remove_from_cart():
    if 'user_info' in session:
        user_info = session['user_info']
        std_id = user_info['id']
        sbj_id = request.json.get('sbj_id')

        conn = pymysql.connect(**config)
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM carttable WHERE std_id=%s AND sbj_id=%s", (std_id, sbj_id))
            conn.commit()
            return jsonify({'message': 'Course removed from cart successfully'}), 200
        except pymysql.MySQLError as e:
            print(f"Error: {e}")
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'User not logged in'}), 401    


@app.route('/buket/search', methods=['GET'])
def search_courses():
    user_info = session.get('user_info')
    if not user_info:
        return jsonify({'error': 'User not logged in'}), 401

    std_id = user_info['id']
    search_input = request.args.get('input', '').lower()

    conn = pymysql.connect(**config)
    try:
        cursor = conn.cursor()
        query = """
            SELECT s.sbj_id, s.subject_name, s.ave_score, s.assignment_amt, s.test_difficulty, 
                   s.lecture_session, s.projects_amt, s.max_std, s.lecture_day, s.lecture_per_week,
                   s.credit, c.priority, c.std_id
            FROM subinfotable s
            LEFT JOIN carttable c ON s.sbj_id = c.sbj_id AND c.std_id = %s
            WHERE LOWER(s.subject_name) LIKE %s
        """
        cursor.execute(query, (std_id, f"%{search_input}%"))
        courses = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify(courses)


if __name__ == '__main__':
    app.run(debug=True)
