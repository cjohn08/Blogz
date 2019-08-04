from flask import Flask, request, redirect, render_template, session   

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:HoopDreams1!@localhost:8889/blogz'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
app.secret_key = "blogging"




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
   allowed_routes = ['login', 'signup', 'index','blog']
   if request.endpoint not in allowed_routes and 'username' not in session:
       return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        username_error = ""
        password_error = ""
        
        if user and user.password == password:
            session['username'] = username
            
            return redirect('/newpost')
        if user and user.password != password:
            password_error = "User password Incorrect"
            
        if not user:
            username_error = "User Does Not Exisit"
        if username_error or password_error:
            return render_template('login.html' , username_error=username_error, password_error=password_error)    
        

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        verify = request.form['verify']
        username_error = ""
        password_error = ""
        verify_error = ""
        
        if verify != password:
           verify_error = "User password Incorrect"
           
        if user :      
            username_error = "User name taken"
            
        if len (username) < 3: 
            username_error = "User name too short" 
           
        if len (password) < 3:
            password_error =  "Password too short"
        if username_error or password_error or verify_error:
            return render_template('signup.html' , username_error=username_error, password_error=password_error, verify_error=verify_error)
        else: 
            newuser = User(username,password)
            db.session.add(newuser)

            db.session.commit()
  
            session['username'] = username
            return redirect('/newpost') 
        

    return render_template('signup.html')



@app.route('/', methods=['GET'])
def index():
    entries = User.query.all()
    return render_template('index.html', entries = entries)
@app.route('/blog', methods=['POST', 'GET'])
def blog():

    blogid = request.args.get('id')
    if blogid:
        singlepost = Blog.query.get(blogid)
        return render_template('SinglePost.html',IndividualPost = singlepost)
    userid = request.args.get('user')
    if userid:
        newuser = Blog.query.filter_by(owner_id=userid).all()
        return render_template('singleuser.html', userposts = newuser)
    entries = Blog.query.all()
        
    return render_template('blogpost.html',entries =entries) 

@app.route('/logout', methods = ['GET'])
def logout():

    del session['username']
    return redirect ('/blog')

@app.route('/newpost', methods=['POST', "GET"])

def newpost():


    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        titleentryerror = ""
        bodyentryerror = ""
        user = User.query.filter_by(username=session['username']).first()
        
        if title == "": 
            titleentryerror = "invalid title entry"
        if body =="":
            bodyentryerror = "invalid body entry"
        if titleentryerror or bodyentryerror:
                return render_template('new_post.html',titleentryerror = titleentryerror, bodyentryerror = bodyentryerror)    
        else:
            newblog = Blog(title,body,user)
            db.session.add(newblog)

            db.session.commit()
            blogid = newblog.id
            return redirect("/blog?id=" + str(blogid))



    return render_template('new_post.html')



if __name__ == '__main__':

    app.run()