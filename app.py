from flask import Flask, request, render_template, redirect, flash, session
from datetime import datetime
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers import response
from details import wordMeaning

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dict.db"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)

#database
class saved(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    word = db.Column(db.String(30),nullable=False)
    date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return f"(word: {self.word}, date_added:{self.date_added})"

db.create_all()

def is_in_saved(word):
    find = saved.query.filter_by(word = word).first()
    if find is None:
        return False
    else:
        return True


#Home route
@app.route('/')
@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'GET':
        session['pword'] = None
        twords = db.session.query(saved).count()
        return render_template('home.html',twords=twords)
    elif request.method == 'POST':
        all = wordMeaning(request.form['search'])
        if all is None:
            flash('The word is not in the dictionary','danger')
            if session['pword'] is None:
                return redirect('/')
            else:
                pword = session['pword']
                return redirect('/link/'+pword)
        else:
            session['pword'] = request.form['search']
            return render_template('home.html',all = all,already_saved=is_in_saved(all[0]['word']))

#saving new word
@app.route('/save/<word>')
def save(word):
    new_word = saved(word=word)
    db.session.add(new_word)
    db.session.commit()
    flash('Word Saved',"success")
    return redirect('/link/'+word)


#deleting from saved word
@app.route('/delete/<here>/<word>')
def delete(word,here):
    got_word = saved.query.filter_by(word=word).first()
    db.session.delete(got_word)
    db.session.commit()
    flash('word deleted','warning')
    if here == 'yes':  
        return redirect('/list')
    else:
        return redirect('/link/'+word)

#list of all saved word
@app.route('/list')
def list():
    all = saved.query.all()
    return render_template('list.html',all=all,title="Word List")

#Route word from hyperlink
@app.route('/link/<word>')
def link(word):
    all = wordMeaning(word)
    session['pword'] = word
    return render_template('home.html',title="WordDiary - "+word,all = all,already_saved=is_in_saved(all[0]['word']))

#running the app
if __name__ == '__main__':
    app.run(debug=True)