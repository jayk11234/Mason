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


@bp.route('/create_ques', methods=["GET","POST"])
@login_required
def create_ques():
    
    if request.method == 'POST':
        db = get_db()
        options=''
        ques = request.form['ques']
        for i in range(1,5):
            options+=request.form['option{num}'.format(num=i)]+","
        error = None
            
        if not ques:
            error = "Question is empty!"

        if error is None:
            db.execute("INSERT INTO quiz (username,quizname,ques,options) VALUES (?,?,?,?)",(g.user['username'],session['quizname'],ques,options,))
            db.commit()

        flash(error)
    return render_template('blog/create_ques.html')


@bp.route('/view_quiz', methods=["GET","POST"])
@login_required
def view_quiz(current_quiz=None,quizname=None):  
    if request.args.get('quizname',None):
        db = get_db()
        quizname=request.args['quizname']
        current_quiz = db.execute("SELECT ques,options FROM quiz WHERE quizname = ?",(quizname,)).fetchall()
    return render_template('blog/view_quiz.html',current_quiz=current_quiz,quizname=quizname)


@bp.route('/user', methods=["GET","POST"])
@login_required
def user():
    db = get_db()
    if request.method == 'POST':
        quizname = request.form['quizname']
        db.execute("INSERT INTO post (username,quizname) VALUES (?,?)",(g.user["username"],quizname,))
        db.commit()
        session['quizname']= quizname
        return redirect(url_for('blog.create_ques'))
    g.quizes = db.execute("SELECT quizname FROM post WHERE username = ? ",(g.user['username'],)).fetchall()
    return render_template('blog/user.html')
        
