from flask import Flask, request, render_template, redirect, url_for, jsonify, session
import pymysql
import pandas as pd
import mpld3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import copy

config = {
    'user' : 'root',
    'password' : 'rlaqhdbs3586!',
    'host' : 'localhost',
    'db' : 'AppClassDB',
    'port' : 3306,
    'cursorclass' : pymysql.cursors.DictCursor
}


def calc_comp(df_ct, df_s, sbj_id):
    max_std_str = df_s[df_s['sbj_id'] == sbj_id]['max_std'].iloc[0]
    max_std_str = max_std_str.split(',')
    grade_list = list(map(int, max_std_str))
    max_std = sum(grade_list)
    now_cart = len(df_ct[df_ct['sbj_id'] == sbj_id])
    comp = now_cart / max_std
    return f"{comp: .2f} : 1"

def calc_rank(df_ct, sbj_id):
    text_list = []
    df_rank = df_ct[df_ct['sbj_id'] == sbj_id].groupby('priority').agg(c=('priority', 'count')).reset_index()
    rank_dict = {i: 0 for i in range(1, 6)} 
    for index, row in df_rank.iterrows():
        pr = row['priority']
        count = row['c']
        if pr in rank_dict:
            rank_dict[pr] = count
    for pr, count in rank_dict.items():
        text_list.append(f"{pr}순위 : {count}명")
    text = ", ".join(text_list)
    return text

def calc_grade(df_ct, df_lg, sbj_id):
    sbj_df = df_ct[df_ct['sbj_id'] == sbj_id]
    grade_dict = {i: 0 for i in range(1, 5)} 
    text_list = []

    for i in sbj_df['std_id']:
        grade = df_lg[df_lg['id'] == i].iloc[0, 1]
        if grade in grade_dict:
            grade_dict[grade] += 1

    for grade, count in grade_dict.items():
        text_list.append(f"{grade}학년 : {count}명")

    text = ", ".join(text_list)
    return text

def rebuild_subs(subinfotable, carttable, logintable):
    subs_copied = [] 
    subinfotable_cp = copy.deepcopy(subinfotable)
    df_ct = pd.DataFrame(carttable)
    df_s = pd.DataFrame(subinfotable)
    df_lg = pd.DataFrame(logintable).drop('pwd', axis=1)  
    for row in subinfotable_cp:
        temp_dict = dict()
        temp_dict['id'] = row.pop('sbj_id')  
        temp_dict['name'] = row.pop('subject_name')  
        temp_dict['competition'] = calc_comp(df_ct, df_s, temp_dict['id'])  
        temp_dict['rankInfo'] = calc_rank(df_ct, temp_dict['id'])  
        temp_dict['gradeInfo'] = calc_grade(df_ct, df_lg, temp_dict['id'])  
        subs_copied.append(temp_dict)
    return subs_copied  

def get_visdata(subs, cartT, lgT, user_id, priority):
    df_subs = rebuild_subs(subs, cartT, lgT)
    df_subs = pd.DataFrame(df_subs)
    df_ct = pd.DataFrame(cartT)
    df_lg = pd.DataFrame(lgT).drop('pwd', axis = 1)
    df_lg = df_lg.rename(columns = {'id' : 'std_id'})
    df_m = df_ct.merge(df_lg)
    try:
        sid = df_m[(df_m['std_id'] == user_id) & (df_m['priority'] == priority)].iloc[0, 1]
    except:
        sid  = df_m[(df_m['std_id'] == user_id) & (df_m['priority'] == 1)].iloc[0, 1]
    r_list = df_subs[df_subs['id'] == sid]['rankInfo'].str.split(', ').to_list()[0]
    g_list = df_subs[df_subs['id'] == sid]['gradeInfo'].str.split(', ').to_list()[0]
    cmp_txt = f"경쟁률 :{df_subs[df_subs['id'] == sid]['competition'].to_list()[0]}"
    
    ranks_x = [1, 2, 3, 4, 5]
    grades_x = [1, 2, 3, 4]
    ranks_y = []
    grades_y = []
    
    for text in r_list:
        pr_dist = text.split(' : ')[1][0]
        ranks_y.append(int(pr_dist))
    for text in g_list:
        gd_dist = text.split(' : ')[1][0]
        grades_y.append(int(gd_dist))
    #now, visualization
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6,10))
    ax1.bar(ranks_x, ranks_y)
    ax1.set_title("priority distribution")
    ax2.bar(grades_x, grades_y)
    ax2.set_title("grade distribution")
    
    graphvis_html = mpld3.fig_to_html(fig)
    plt.close(fig)
    cmp_txt_html = f"<h4>{cmp_txt}</h4>"
    graphvis_html = cmp_txt_html + graphvis_html
    return graphvis_html

def get_subject_scores(std_id):
    conn = pymysql.connect(**config)
    scores = []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT sbj_id FROM carttable WHERE std_id=%s ORDER BY priority", (std_id,))
        cart_subjects = cursor.fetchall()
        
        for subject in cart_subjects:
            sbj_id = subject['sbj_id']
            cursor.execute("SELECT ave_score, assignment_amt, test_difficulty, lecture_session, projects_amt FROM subInfoTable WHERE sbj_id=%s", (sbj_id,))
            sub_info = cursor.fetchone()
            
            if sub_info:
                scores.append([
                    sub_info['ave_score'],
                    sub_info['assignment_amt'],
                    sub_info['test_difficulty'],
                    sub_info['lecture_session'],
                    sub_info['projects_amt']
                ])
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return scores