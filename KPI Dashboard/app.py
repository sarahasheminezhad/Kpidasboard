from flask import Flask, render_template, jsonify
import pandas as pd
from models import db, User
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

barname_df = pd.read_excel("static/data/barname.xlsx")

app = Flask(__name__)
app.config["SECRET_KEY"] = "یه رمز خیلی طولانی"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"

db.init_app(app)
login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"
@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))

df = pd.read_excel("static/data/1404-03.xlsx")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/ranking")
def ranking():
    return jsonify(df.to_dict(orient="records"))

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()


        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("my_dashboard"))

        return render_template(
            "login.html",
            error="نام کاربری یا رمز عبور اشتباه است."
        )

    return render_template("login.html")




@app.route("/my-dashboard")
@login_required
def my_dashboard():

    my_data = barname_df[
        barname_df["بازاریاب"] == current_user.marketer
    ]

    return render_template(

        "my_dashboard.html",

        user=current_user,

        data=my_data.to_dict(orient="records"),

        total_waybills=len(my_data),

        total_customers=my_data["فرستنده"].nunique(),

        total_weight=my_data["وزن"].sum()

    )


@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect("/")


with app.app_context():
    db.create_all()
if __name__ == "__main__":
    
    app.run(debug=True)