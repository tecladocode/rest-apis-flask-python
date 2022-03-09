from flask import abort, request
from flask_restx import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel
from schemas import ItemSchema

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item)
        abort(404, "Item not found")

    @jwt_required(fresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            abort(400, f"An item with name {name} already exists.")

        data = item_schema.load(request.get_json())

        item = ItemModel(name=name, **data)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, "An error occurred while inserting the item.")

        return item_schema.dump(item), 201

    @jwt_required()
    def delete(self, name):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            abort(401, "Admin privilege required.")

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}
        abort(404, "Item not found.")

    def put(self, name):
        data = item_schema.load(request.get_json())

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item_schema.dump(item)


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = ItemModel.find_all()
        if user_id:
            return items_schema.dump(items), 200
        return {
            "items": [item.name for item in items],
            "message": "More data available if you log in.",
        }, 200
