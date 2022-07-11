from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:name>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store
        abort(404, message="Store not found.")

    @blp.response(201, StoreSchema)
    def post(cls, name):
        if StoreModel.find_by_name(name):
            abort(400, message=f"A store with name '{name}' already exists.")

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store

    def delete(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted"}, 200
        abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return StoreModel.find_all()
