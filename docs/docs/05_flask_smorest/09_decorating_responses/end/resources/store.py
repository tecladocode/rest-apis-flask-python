import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema


blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(cls, store_id):
        try:
            # You presumably would want to include the store's items here too
            # More on that when we look at databases
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(cls, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(cls, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store
