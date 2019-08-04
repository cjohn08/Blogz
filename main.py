from flask import Flask, request, redirect, render_template, session   

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:HoopDreams1!@localhost:8889/blogz'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)





class Blog(db.Model):



    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))   
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id')) 





    def __init__(self,title,body,owner):

        self.title = title

        self.body = body

        self.owner = owner
class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(120), unique=True)
   password = db.Column(db.String(120))
   blogs = db.relationship('Blog', backref='owner')
   def __init__(self, username, password):
       self.username = username
       self.password = password

@app.before_request
def require_login():
   allowed_routes = ['login', 'register']
   if request.endpoint not in allowed_routes and 'email' not in session:
       return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged In")
            return redirect('/newpost')
        if user and user.password != password:
            flash("User password Incorrect", "error")
            return redirect('/login')
        if not user:
            flash("User Does Not Exisit", "error")
            return redirect('/login')    
        

    return render_template('login.html')





@app.route('/login', methods=['POST', 'GET'])
def index():

    blogid = request.args.get('id')
    if blogid:
        singlepost = Blog.query.get(blogid)
        return render_template('SinglePost.html',IndividualPost = singlepost)
    entries = Blog.query.all()
    
    return render_template('todos.html',entries =entries) 




@app.route('/newpost', methods=['POST', "GET"])

def newpost():


    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        titleentryerror = ""
        bodyentryerror = ""
        if title == "": 
            titleentryerror = "invalid title entry"
        if body =="":
            bodyentryerror = "invalid body entry"
        if titleentryerror or bodyentryerror:
                return render_template('new_post.html',titleentryerror = titleentryerror, bodyentryerror = bodyentryerror)    
        else:
            newblog = Blog(title,body)
            db.session.add(newblog)

            db.session.commit()
            blogid = newblog.id
            return redirect("/blog?id=" + str(blogid))



    return render_template('new_post.html')



if __name__ == '__main__':

    app.run()