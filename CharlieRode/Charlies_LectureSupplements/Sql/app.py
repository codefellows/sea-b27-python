from flask import Flask
import psycopg2

app= Flask(__name__)
conn= psycopg2.connect(host="localhost", port=5432, user="codefellows", password="password")

@app.route("/students")
def show_students():
    with (conn.cursor()) as cur:
        cur.execute("SELECT first_name, last_name FROM Students")
        rs= cur.fetchall()
        return str(rs)

#@app.route("/echo/<text>")
#def ech_text(text):
    #return "You said: " + text

if __name__ == "__main__":
    app.run()