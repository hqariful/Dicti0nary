from Models import Base, User, Words
from sqlalchemy.orm import Session as SS
from connect import engine
from datetime import datetime
from details import wordMeaning
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

ss = SS(bind=engine)
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#database
# class saved(ss.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     word = db.Column(db.String(30),nullable=False)
#     date_added = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

#     def __repr__(self):
#         return f"(word: {self.word}, date_added:{self.date_added})"


def is_in_saved(word):
    u1 = ss.query(User).filter(User.id==session["user_id"]).first()
    w1 = ss.query(Words).filter(Words.word==word).first()
    return w1 in u1.words

@app.route("/")
@app.route("/register",methods = ["GET","POST"])
def register(err_msg = ""):
    if request.method == "POST":
        usr = request.form["usr"]
        usr = ss.query(User).filter(User.username == usr).first()
        if usr:
            err_msg = "user already exists"
        else:
            ss.add(User(username = request.form["usr"],
                        password = request.form["pwd"],
                        email = request.form["email"]))
            ss.commit()
            err_msg = "New User Added"
            return redirect(url_for("login",err_msg=err_msg))
    if "user_id" in session:
        return redirect(url_for("home"))
    else:
        return render_template("register.html",err_msg=err_msg)

@app.route("/login", methods = ["GET", "POST"])
def login(err_msg = ""):
    if request.method == "POST":
        usr = request.form["usr"]
        usr = ss.query(User).filter(User.username == usr).first()
        if usr:
            if usr.password == request.form["pwd"]:
                print("login initiated")
                session["user_id"] = usr.id
                return redirect("home")
            else:
                err_msg = "login failed"
        else:
            err_msg = "No user with this username"
    if "user_id" in session:
        return redirect(url_for("home"))
    else:
        return render_template("login.html",err_msg = err_msg)
    
@app.route("/logout")
def logout():
    session.pop("user_id",None)
    return redirect(url_for("login"))

@app.route("/home",methods=['GET','POST'])
def home(msg=""):
    if "user_id" in session:
        if request.method == 'GET':
            usr = ss.query(User).filter(User.id == session["user_id"]).first()
            words = ss.query(Words).filter(Words.user_id == session["user_id"]).all()
            print(f"session = {session["user_id"]},user = {usr},words {words},tword = {len(words)}")
            session['pword'] = None
            return render_template('home.html',usr =usr,twords=len(words))
        
        elif request.method == 'POST':
            all = wordMeaning(request.form['search'])
            print(all)
            if all is None:
                msg = ('The word is not in the dictionary','warning')
                if session['pword'] is None:
                    return redirect('/',msg=msg[0])
                else:
                    pword = session['pword']
                    return redirect('/link/'+pword)
            else:
                session['pword'] = request.form['search']
                return render_template('home.html',all = all,already_saved=is_in_saved(all[0]['word']))
    else:
        return redirect(url_for("login"))
    
@app.route("/setting")
def setting():
    if "user_id" in session:
        usr = ss.query(User).filter(User.id==session["user_id"]).first()
        return render_template("setting.html",usr=usr,own=True)
    else:
        return redirect(url_for("login"))    

# #Home route
# @app.route('/')
# @app.route('/search',methods=['GET','POST'])
# def search():
    # if request.method == 'GET':
    #     session['pword'] = None
    #     twords = ss.session.query(saved).count()
    #     return render_template('home.html',twords=twords)
#     elif request.method == 'POST':
#         all = wordMeaning(request.form['search'])
#         if all is None:
#             flash('The word is not in the dictionary','danger')
#             if session['pword'] is None:
#                 return redirect('/')
#             else:
#                 pword = session['pword']
#                 return redirect('/link/'+pword)
#         else:
#             session['pword'] = request.form['search']
#             return render_template('home.html',all = all,already_saved=is_in_saved(all[0]['word']))

#saving new word
@app.route('/save/<word>')
def save(word):

    w = Words(user_id=session["user_id"],word=word,time_posted=datetime.now())
    ss.add(w)
    ss.commit()
    msg = 'Word Saved',"success"
    return redirect('/link/'+word)


#deleting from saved word
@app.route('/delete/<here>/<word>')
def delete(word,here):
    got_word = ss.query(Words).filter(Words.word==word).first()
    ss.delete(got_word)
    ss.commit()
    msg = 'word deleted','warning'
    if here == 'yes':  
        return redirect('/list')
    else:
        return redirect('/link/'+word)

#list of all saved word
@app.route('/list')
def list():
    all = ss.query(Words).filter(Words.user_id==session["user_id"])
    return render_template('list.html',all=all,title="Word List")

#Route word from hyperlink
@app.route('/link/<word>')
def link(word):
    all = wordMeaning(word)
    session['pword'] = word
    print(is_in_saved(all[0]['word']))
    return render_template('home.html',title="WordDiary - "+word,all = all,already_saved=is_in_saved(all[0]['word']))

#running the app
if __name__ == '__main__':
    app.run(debug=True)