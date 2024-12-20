from rabbitmq import connect_rabbitmq, send_message
import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Food(db.Model):
    __tablename__ = "foods"

    name = db.Column(db.String(25), primary_key=True)
    restaurant = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(255), nullable=False)

    def _init_(self, name, restaurant, price, calories, category):
        self.name = name
        self.restaurant = restaurant
        self.price = price
        self.calories = calories
        self.category = category

    @classmethod
    def add_food(cls, food_data):
        food = {
            "name": food_data["name"],
            "restaurant": food_data["restaurant"],
            "price": food_data["price"],
            "calories": food_data["calories"],
            "category": food_data["category"],
        }
        send_message_to_queue(food)

        return food["name"]

    @classmethod
    def get_food(cls, name):
        food = cls.query.filter_by(name=name).first()
        return food.to_dict() if food else None

    @classmethod
    def get_all_foods(cls):
        foods = cls.query.all()
        return [food.to_dict() for food in foods]

    def to_dict(self):
        return {
            "name": self.name,
            "restaurant": self.restaurant,
            "price": self.price,
            "calories": self.calories,
            "category": self.category,
        }


def send_message_to_queue(food_data):
    channel = connect_rabbitmq()
    send_message(channel, "food_queue", food_data)
    channel.close()
