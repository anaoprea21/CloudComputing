from flask_restful import Resource, reqparse
import os
import redis
from models import Food

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_DATABASE = os.getenv("REDIS_DATABASE", "0")
redis_client = redis.StrictRedis(
    host=REDIS_HOST, db=REDIS_DATABASE, decode_responses=True
)

parser = reqparse.RequestParser()
parser.add_argument("name", required=True, help="name of the food cannot be blank")
parser.add_argument(
    "restaurant", required=True, help="restaurant of the food cannot be blank"
)
parser.add_argument("price", required=True, help="calories must be a number")
parser.add_argument(
    "calories", type=int, required=True, help="calories must be a number"
)
parser.add_argument(
    "category", required=True, help="category of the food cannot be blank"
)


class FoodAPI(Resource):
    def get(self, name):
        food = Food.get_food(name)
        if food:
            redis_key = f"food:{name}:access_count"
            redis_client.incr(redis_key)
            access_count = redis_client.get(redis_key)

            food["access_count"] = access_count
            return food, 200
        return {"message": "Food not found"}, 404


class FoodsAPI(Resource):
    def get(self):
        return Food.get_all_foods(), 200

    def post(self):
        args = parser.parse_args()
        food = {
            "name": args["name"],
            "restaurant": args["restaurant"],
            "price": args["price"],
            "calories": args["calories"],
            "category": args["category"],
        }
        index = Food.add_food(food)
        return {"index": index}, 201
