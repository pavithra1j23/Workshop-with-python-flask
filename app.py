from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


def create_database():
    db = sqlite3.connect("users.db")
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    db.commit()
    db.close()


@app.route("/")
def welcome():
    return render_template("welcome.html")


@app.route("/submit", methods=["POST"])
def submit():

    username = request.form.get("username")
    email = request.form.get("email")
    print("USERNAME =", username)
    print("EMAIL =", email)
    db = sqlite3.connect("users.db")
    cur = db.cursor()
    cur.execute(
        "INSERT INTO users (username, email) VALUES (?, ?)",
        (username, email)
    )

    db.commit()
    db.close()

    return redirect("/workshops")


@app.route("/workshops")
def workshops():
    return render_template("workshops.html")


@app.route("/admin")
def admin():

    db = sqlite3.connect("users.db")
    cur = db.cursor()
    cur.execute("SELECT id, username, email FROM users")
    users = cur.fetchall()
    db.close()
    return render_template("admin.html", users=users)


@app.route("/delete/<int:id>")
def delete(id):

    db = sqlite3.connect("users.db")
    cur = db.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (id,))
    db.commit()
    db.close()

    return redirect("/admin")

if __name__ == "__main__":
    create_database()
    app.run(debug=True)
