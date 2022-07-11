from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:name>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item
        abort(404, message="Item not found")

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data, name):
        if ItemModel.find_by_name(name):
            abort(400, message=f"An item with name {name} already exists.")

        item = ItemModel(**item_data, name=name)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item

    @jwt_required()
    def delete(self, name):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            abort(401, message="Admin privilege required.")

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}
        abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_data["price"]
        else:
            item = ItemModel(name, **item_data)

        item.save_to_db()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.find_all()
