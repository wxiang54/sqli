from flask import Flask, render_template, session, url_for, request
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    db = sqlite3.connect("data/db.db")
    c = db.cursor()

    if request.method == "GET":
        q = "SELECT name FROM sqlite_master WHERE type='table';"
        c.execute(q)
        list_tableNames = map((lambda table: str(table[0])), c.fetchall())
        
        if 'thinker' not in list_tableNames:
            print "\n\nTHINKER DROPPED\n\n"
            q = '''
            CREATE TABLE thinker (
            id INTEGER PRIMARY KEY,
            username VARCHAR(50) UNIQUE,
            password VARCHAR(50)
            );
            '''
            c.execute(q)
            q = "INSERT INTO thinker VALUES(1, 'top','kek');"
            c.execute(q)
            q = "INSERT INTO thinker VALUES(2, 'a','b');"
            c.execute(q)
            db.commit()
        return render_template("index.html")

    else: 
        username = request.form.get("username")
        password = request.form.get("password")
        q = "SELECT * FROM thinker WHERE username = '" + username + "' AND password = '" + password + "';"
        
        users = c.execute(q)
        return q
        return str(users.fetchall())
        if users:
            return "Successfully logged in!"
        else:
            return "Invalid login!"

if __name__ == "__main__":
    app.debug = True
    app.run()
