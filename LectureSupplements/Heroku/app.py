from flask import Flask, render_template
import os, psycopg2, urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.getenv("DATABASE_URL"))

app = Flask(__name__)

conn = psycopg2.connect(
    database = url.path[1:],
    user = url.username,
    password = url.password,
    host = url.hostname,
    port = url.port)

@app.route("/hello/<name>")
def hello(name):
    return "Hello, " + name + "!"

@app.route("/students")
def get_students():
    cur = conn.cursor()
    cur.execute("SELECT first_name, last_name FROM Students")
    rs = cur.fetchall()
    return render_template("students.html", students=rs)
    

if __name__ == "__main__":
    app.run()
