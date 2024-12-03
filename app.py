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


@app.route("/food/add", methods=["GET", "POST"])
def add_food_route():
    form = FoodForm()
    if form.validate_on_submit():
        food = {
            "name": form.name.data,
            "restaurant": form.restaurant.data,
            "price": form.price.data,
            "calories": form.calories.data,
            "category": form.category.data,
        }
        Food.add_food(food)
        return redirect(url_for("index"))
    return render_template("add_food.html", form=form)


@app.route("/food/view", methods=["GET", "POST"])
def view_food_route():
    form = ViewFoodForm()
    if form.validate_on_submit():
        name = form.name.data
        return redirect(f"/api/food/{name}")

    return render_template("view_food.html", form=form)


api.add_resource(FoodAPI, "/api/food/<string:name>")
api.add_resource(FoodsAPI, "/api/foods")

if __name__ == "__main__":
    app.run(debug=True)
