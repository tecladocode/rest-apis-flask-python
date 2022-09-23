from flask import abort
from flask_restx import Namespace, Resource, fields
from sqlalchemy.exc import SQLAlchemyError
from models import StoreModel


api = Namespace("stores", description="Operations related to stores.")

nested_item = api.model(
    "NestedItem",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "price": fields.Float(),
    },
)

store_outputs = api.model(
    "Store",
    {
        "id": fields.Integer(),
        "name": fields.String(),
        "items": fields.List(fields.Nested(nested_item)),
    },
)


@api.route("/<name>")
class Store(Resource):
    @api.marshal_with(store_outputs)
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store
        abort(404, "Store not found.")

    @api.marshal_with(store_outputs)
    def post(self, name):
        if StoreModel.find_by_name(name):
            abort(400, f"A store with name '{name}' already exists.")

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except SQLAlchemyError:
            abort(500, "An error occurred creating the store.")

        return store, 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted"}, 200
        abort(404, "Store not found.")


@api.route("/")
class StoreList(Resource):
    @api.marshal_list_with(store_outputs)
    def get(self):
        return StoreModel.find_all()
