from flask import Flask, request, redirect, render_template

from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:basketball@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)





class Blog(db.Model):



    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(120))

    body = db.Column(db.String(1000))



    def __init__(self,title,body):

        self.title = title

        self.body = body



@app.route("/blog", methods=['POST','GET'])

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