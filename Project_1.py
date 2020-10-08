from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/theflaskapp"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Registers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    email = db.Column(db.String(30))
    phone = db.Column(db.BIGINT)


db.create_all()


@app.route("/")
def index():
    return render_template("layout.html")


@app.route("/list", methods=['GET'])
def reg_list():
    result = Registers.query.all()
    return render_template("list.html", res=result)


@app.route("/reg")
def reg():
    return render_template("registry.html", users=None,action="process")


@app.route("/process", methods=["POST"])
def process():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    phone = request.form["phone"]

    users = Registers(first_name=firstname, last_name=lastname, email=email, phone=phone)
    db.session.add(users)
    db.session.commit()

    return redirect(url_for("reg_list"))


@app.route("/delete/<user_id>", methods=["get"])
def delete(user_id):
    user = Registers.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("reg_list"))


@app.route("/edit/<user_id>", methods=["get"])
def edit(user_id):
    user = Registers.query.get(user_id)
    return render_template("registry.html", users=user, action="update")


@app.route("/update", methods=["post"])
def update():
    user_id = request.form["id"]
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    phone = request.form["phone"]

    user = Registers.query.get(user_id)
    user.first_name = firstname
    user.last_name = lastname
    user.email = email
    user.phone = phone
    db.session.commit()

    return redirect(url_for("reg_list"))


if __name__ == "__main__":
    app.run()
