from flask import Flask, render_template, session, url_for, request, redirect
import os.path
import hashlib
import sqlite3

app = Flask(__name__)
path = "/var/www/FlaskApp/sqli/data/"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo", methods=["GET", "POST"])
def demo():
    #MODIFY THIS LINE
    session["search"] = True
    
    if not os.path.isfile(path + "injectMe.db"):
        db = sqlite3.connect(path + "injectMe.db")
        c = db.cursor()
        q = '''
            CREATE TABLE user (
            id INTEGER PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            age INTEGER,
            numFriends INTEGER,
            isSingle INTEGER,
            timeJoined INTEGER,
            password VARCHAR(50)
            );
        '''
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('demo', 42, 2048, 0, 0, '%s');" % (hashlib.sha256("demo").hexdigest())
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('john doe', 22, 5, 1, 11, '%s');" % (hashlib.sha256("password").hexdigest())
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('jane doe', 19, 9, 1, 13, '%s');" % (hashlib.sha256("possword").hexdigest())
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('jonathon doe', 19, 9, 0, 13, '%s');" % (hashlib.sha256("xdxd").hexdigest())
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('magnanimous gas', 404, 404, 0, 404, '%s');" % (hashlib.sha256("alternativeFacts").hexdigest())
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('i got lazy', 404, 404, 0, 404, '%s');" % (hashlib.sha256("alternativeF").hexdigest())
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('tis 5:16 am', 404, 404, 1, 404, '%s');" % (hashlib.sha256("alternatiacts").hexdigest())
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('need more ppl', 404, 404, 0, 404, '%s');" % (hashlib.sha256("alternaFacts").hexdigest())
        c.execute(q)
        q = "INSERT INTO user(username, age, numFriends, isSingle, timeJoined, password) VALUES('and anotha one', 404, 404, 0, 404, '%s');" % (hashlib.sha256("khaled").hexdigest())
        c.execute(q)
        db.commit()
    else:
        db = sqlite3.connect(path + "injectMe.db")
        c = db.cursor()

        
    if request.method == "GET":
        if "username" not in session:
            return render_template("login.html")
        else:
            return render_template("home.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        password = hashlib.sha256(password).hexdigest()
        q = "SELECT * FROM user WHERE username = '" + username + "' AND password = '" + password + "';"
        
        users = c.execute(q).fetchall()
        if users:
            session['username'] = users[0][1];
            return render_template("home.html");
        else:
            return render_template("login.html", error="Username and/or password is incorrect!")


@app.route('/demo/logout')
def logout():
    session.pop('username', None)
    session.pop('search', None)
    return redirect( url_for("demo") )
        

@app.route('/demo/search', methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return redirect( url_for("demo") )
    
    db = sqlite3.connect(path + "injectMe.db")
    c = db.cursor()
    query = request.form.get("search")
    if query and query != " ":
        q = "SELECT username, age, numFriends, isSingle, timeJoined FROM user WHERE username LIKE '%" + query + "%';"
        print q
        users = c.execute(q).fetchall()
    else:
        users = ()
    usersParsed = []
    for user in users:
        d = {}
        d['username'] = user[0]
        d['age'] = user[1]
        d['numFriends'] = user[2]
        d['isSingle'] = user[3]
        d['timeJoined'] = user[4]
        usersParsed.append(d)
    return render_template("home.html", searchResults=usersParsed)
        
if __name__ == "__main__":
    app.debug = True
    app.run()
