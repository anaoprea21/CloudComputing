from flask import Flask, render_template, redirect, url_for, flash
from flask_restful import Api
from faker import Faker
from faker.providers import BaseProvider
import os
import psycopg

from resources import FoodAPI, FoodsAPI
from forms import FoodForm, ViewFoodForm
from models import db, Food

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USERNAME = os.getenv("DB_USERNAME", "postgres")

DB_PASSWORD = os.getenv("DB_PASSWORD", "my-secret-pw")
DB_NAME = os.getenv("DB_NAME", "db")

app = Flask(__name__)
api = Api(app)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql+psycopg://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config["SECRET_KEY"] = "SECRET_KEY"

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/food/populate", methods=["GET"])
def populate_foods():
    fake = Faker()
    food = {
        "name": "Pizza",
        "restaurant": "fds",
        "price": fake.random_int(min=20, max=100),
        "calories": fake.random_int(min=20, max=100),
        "category": "bread",
    }
    Food.add_food(food)
    food1 = {
        "name": "Burger",
        "restaurant": "dfs",
        "price": fake.random_int(min=20, max=100),
        "calories": fake.random_int(min=20, max=100),
        "category": "bread",
    }
    Food.add_food(food1)
    food2 = {
        "name": "Miso Soupe",
        "restaurant": "df",
        "price": fake.random_int(min=20, max=100),
        "calories": fake.random_int(min=20, max=100),
        "category": "soupe",
    }
    Food.add_food(food2)
    flash("3 new foods have been added successfully!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
