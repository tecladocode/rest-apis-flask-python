from flask import abort
from flask_restx import Resource
from sqlalchemy.exc import SQLAlchemyError
from models import StoreModel
from schemas import StoreSchema


store_schema = StoreSchema()
stores_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    def get(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store)
        abort(404, "Store not found.")

    @classmethod
    def post(cls, name):
        if StoreModel.find_by_name(name):
            abort(400, f"A store with name '{name}' already exists.")

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except SQLAlchemyError:
            abort(500, "An error occurred creating the store.")

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted"}, 200
        abort(404, "Store not found.")


class StoreList(Resource):
    @classmethod
    def get(cls):
        return stores_schema.dump(StoreModel.find_all())
