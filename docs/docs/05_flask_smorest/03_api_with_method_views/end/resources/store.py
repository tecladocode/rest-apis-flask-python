import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores


blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/stores/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            # You presumably would want to include the store's items here too
            # More on that when we look at databases
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")


@blp.route("/stores")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(
                400,
                message="Bad request. Ensure 'name' is included in the JSON payload.",
            )
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(400, message=f"Store already exists.")

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store

        return store
