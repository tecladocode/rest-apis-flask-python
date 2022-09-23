from flask import request
from flask_restx import Namespace, Resource, fields, abort
from flask_jwt_extended import jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import ItemModel

api = Namespace("items", description="Operations related to store items.")

item_inputs = api.model(
    "ItemFields",
    {
        "price": fields.Float(required=True, description="A price for this item."),
        "store_id": fields.Integer(
            required=True,
            description="The identifier for the store that this item belongs to.",
        ),
    },
)

nested_resource = api.model(
    "NestedResource", {"id": fields.Integer(), "name": fields.String()}
)

item_outputs = api.inherit(
    "Item",
    item_inputs,
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "store": fields.Nested(nested_resource),
        "tags": fields.List(fields.Nested(nested_resource)),
    },
)


@api.route("/<name>")
@api.param("name", "The unique name for the item you want to interact with.")
@api.doc(
    responses={
        404: "Item not found.",
        400: "Bad request (name already exists or validation error).",
        500: "An error occurred while inserting that item.",
    }
)
class Item(Resource):
    @jwt_required()
    @api.marshal_with(item_outputs)
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item
        abort(404, "Item not found")

    @jwt_required(fresh=True)
    @api.expect(item_inputs, validate=True)
    @api.marshal_with(item_outputs)
    def post(self, name):
        if ItemModel.find_by_name(name):
            abort(400, f"An item with name {name} already exists.")

        item = ItemModel(name=name, **request.get_json())

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, "An error occurred while inserting the item.")

        return item, 201

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

    @api.expect(item_inputs, validate=True)
    @api.marshal_with(item_outputs)
    def put(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.price = request.get_json()["price"]
        else:
            item = ItemModel(name, **request.get_json())

        item.save_to_db()
        return item


@api.route("/")
class ItemList(Resource):
    @api.marshal_list_with(item_outputs)
    def get(self):
        items = ItemModel.find_all()
        return items, 200
