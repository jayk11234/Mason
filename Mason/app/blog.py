import functools
from flask import (g,flash,Blueprint,redirect,url_for,render_template,request,session)
from app.db import get_db
from werkzeug.security import check_password_hash,generate_password_hash
from app.auth import login_required

bp = Blueprint('blog',__name__)

@bp.route('/')  
@login_required
def index():
    return render_template('blog/index.html')


@bp.route('/<username>/<quizname>/add_ques', methods=["GET","POST"])
@login_required
def create_ques(username,quizname):
    
    if request.method == 'POST':
        db = get_db()
        options=''
        ques = request.form['ques']
        for i in range(1,5):
            options+=request.form['option{num}'.format(num=i)]+","
        ans = request.form['answer']
        error = None
            
        if not ques:
            error = "Question is empty!"

        if error is None:
            db.execute("INSERT INTO quiz (username,quizname,ques,options) VALUES (?,?,?,?)",(username,quizname,ques,options,))
            db.commit()
            db.execute("INSERT INTO quiz_answers (username,quizname,ques,ans) VALUES (?,?,?,?)",(username,quizname,ques,ans,))
            db.commit()
        flash(error)
    return render_template('blog/create_ques.html')



@bp.route('/user', methods=["GET","POST"])
@login_required
def user():
    db = get_db()
    username=g.user["username"]
    if request.method == 'POST':
        quizname = request.form['quizname']
        if(quizname != ''):
            db.execute("INSERT INTO post (username,quizname) VALUES (?,?)",(username,quizname,))
            db.commit()
            session['quizname']= quizname
            return redirect(url_for('blog.create_ques',username=username,quizname=quizname))
    g.quizes = db.execute("SELECT quizname FROM post WHERE username = ? ",(username,)).fetchall()
    return render_template('blog/user.html')


@bp.route('/<username>/<quizname>', methods=["GET","POST"])
@login_required
def view_quiz(username,quizname):  
    db = get_db()
    #quizname=request.args['quizname']
    current_quiz = db.execute("SELECT ques,options FROM quiz WHERE quizname = ? AND username = ?",(quizname,username,)).fetchall()
    if request.method=="POST":
            score=0
            i=1
            for ques in current_quiz:
                ans = db.execute("SELECT ans FROM quiz_answers WHERE username = ? AND quizname= ? AND ques = ?",(username,quizname,ques['ques'])).fetchone()
                #to print score on submitting quiz
                if ans['ans']== request.form['ques{num}'.format(num=i)]: 
                    score+=1
                    print(score)
            return render_template('blog/score.html',score=score)
    return render_template('blog/view_quiz.html',current_quiz=current_quiz,quizname=quizname)


@bp.route('/<username>/<quizname>/update', methods=["GET","POST"])
@login_required
def update_quiz(username,quizname):
    db = get_db()
    current_quiz = db.execute("SELECT ques,options FROM quiz WHERE quizname = ? AND username = ?",(quizname,username,)).fetchall()
    quiz_answers = db.execute("SELECT ans FROM quiz_answers where username = ? AND quizname = ?",(quizname,username,)).fetchall()
    
    if request.method=="POST":
        i=1
        for question in current_quiz:
            formerquestion=question['ques'] #original ques
            opts = question['options'].split(',') #original options in the form of list
            ques = request.form['ques{num}'.format(num=i)] 
            
            if ques == "": #if user does not update question original question is used
                ques = formerquestion
            #to store updated answer
            ans = request.form['answer{num}'.format(num=i)]
            
            options=""  
            for j in range(1,5): 
                print(j)
                opt = request.form['ques{num1}-option{num2}'.format(num1=i,num2=j)]
                if opt == "":
                    options+=opts[j-1]+","  #if user does not update original options are used
                else:
                    options+=opt+","
                print(options)
            db.execute('UPDATE quiz_answers SET ques = ?, ans = ? WHERE username = ? AND quizname = ? AND ques = ? ',(ques,ans,username,quizname,formerquestion,))
            db.commit()
            db.execute('UPDATE quiz SET ques = ?, options = ? WHERE username = ? AND quizname = ? AND ques = ? ',(ques,options,username,quizname,formerquestion,))
            db.commit()
            i+=1
    return render_template('blog/update.html',quizname=quizname,current_quiz=current_quiz,quiz_answers=quiz_answers,length=len(current_quiz))

    

@bp.route('/<username>/<quizname>/delete', methods=["POST"])
@login_required
def delete_quiz(username,quizname):
    db=get_db()
    db.execute("DELETE FROM quiz_answers WHERE username= ? AND quizname = ?",(username,quizname,))
    db.execute("DELETE FROM quiz WHERE username= ? AND quizname = ?",(username,quizname,))
    db.execute("DELETE FROM post WHERE username= ? AND quizname = ?",(username,quizname,))
    db.commit()
    return redirect(url_for('blog.user'))
    
    

