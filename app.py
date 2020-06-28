from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

# Database
import os
from flask_sqlalchemy import SQLAlchemy

from forms import WeightEntryForm, FoodEntryForm

from dotenv import load_dotenv
from utility import make_float, create_plot, parse_dates
from datetime import datetime

load_dotenv()


app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config["SECRET_KEY"] = "secret"

# Database settings
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# initialise database migrations
migrate = Migrate(app, db)

# adding a shell context
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


class WeightEntry(db.Model):
    __tablename__ = "weight"
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float())
    user = db.Column(db.String(64))
    date = db.Column(db.Date())


class FoodEntry(db.Model):
    __tablename__ = "food_log"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(240))
    meal_type = db.Column(db.String(20))
    consume_date = db.Column(db.Date())
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def index():

    return render_template("index.html")
    # return "<h1>Hello World</h1>"


@app.route("/weight", methods=["GET", "POST"])
def weight():
    form = WeightEntryForm()
    bar = create_plot()
    if form.validate_on_submit():
        weight_log = WeightEntry(
            weight=make_float(form.weight.data),
            user=form.user.data,
            date=parse_dates(form.date.data),
        )
        db.session.add(weight_log)
        db.session.commit()
        flash("item saved to database")
        return redirect(url_for("weight"))
    return render_template("weight.html", form=form, plot=bar)


@app.route("/food", methods = ["GET", "POST"])
def food():

    form = FoodEntryForm()
    logs = FoodEntry.query.limit(10).all()
    if form.validate_on_submit():
        food_log = FoodEntry(
            description = form.description.data,
            meal_type = form.meal_type.data,
            consume_date = parse_dates(form.consume_date.data)
        )
        db.session.add(food_log)
        db.session.commit()
        return redirect(url_for("food"))
    return render_template("food.html", form=form, food_logs=logs)
