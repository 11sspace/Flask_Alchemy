from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__, template_folder="flask")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class mist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    date = db.Column(db.DateTime)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        data = mist.query.all()
        return render_template("index.html", data=data)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        data = request.form["work"]
        todo = mist(task=data, date=datetime.now())
        db.session.add(todo)
        db.session.commit()
        print("Added ")
        return redirect("/")


@app.route("/delete/<string:id>")
def delete(id):
    dlt = mist.query.get(id)  # or404
    db.session.delete(dlt)
    db.session.commit()
    print("deleted")
    return redirect("/")


@app.route("/update/<string:id>", methods=["GET", "POST"])
def update(id):
    dlt = mist.query.get(id)
    if request.method == "GET":
        print("It is a get method")

        data = mist.query.all()
        return render_template("index.html", update_fun=dlt, data=data)
    else:
        dlt.task = request.form['work']
        db.session.commit()
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
