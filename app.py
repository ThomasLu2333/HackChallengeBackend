import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)

def success(data, status_code):
    return json.dumps(data), status_code


def error(message, status_code):
    return json.dumps({"error": message}), status_code

@app.route("/locations/")
def get_locations():
    return success({"locations": DB.get_locations()}, 200)


@app.route("/restaurants/<int:location_id>/")
def get_restaurant_from_location(location_id):
    if DB.get_location(location_id) is None:
        return error("location doesn't exist", 404)
    return success({"restaurants": DB.get_restaurants_of_location(location_id)}, 200)


@app.route("/restaurant/<int:restaurant_id>/")
def get_restaurant(restaurant_id):
    if DB.get_restaurant(restaurant_id) is None:
        return error("restaurant doesn't exist", 404)
    return success(DB.get_restaurant(restaurant_id), 200)


@app.route("/restaurants/", methods=["POST"])
def create_restaurant():
    body = json.loads(request.data)
    name, description, location_id, cuisine, address, image, rating = (
        body.get("name"), body.get("description"), body.get("location_id"), body.get("cuisine"), body.get("address"),
        body.get("image"), body.get("rating", 3)
    )
    if name is None or description is None or location_id is None or address is None or rating is None:
        return error("missing fields in POST /restaurants/", 400)
    if (not isinstance(name, str) or not isinstance(description, str) or not isinstance(location_id, int)
            or not isinstance(address, str) or not isinstance(rating, int) or not (1 <= rating <= 5)
            or DB.get_location(location_id) is None):
        return error("invalid fields in POST /restaurants/", 400)
    return success(DB.create_restaurant(name=name, description=description, location_id=location_id, address=address,
                                        image=image, rating=rating, cuisine=cuisine), 201)


@app.route("/restaurants/<int:restaurant_id>/", methods=["DELETE"])
def delete_review(restaurant_id):
    rest = DB.get_restaurant(restaurant_id)
    if rest is None:
        return error("restaurant does not exist", 404)
    DB.delete_review(restaurant_id)
    return success(rest, 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
