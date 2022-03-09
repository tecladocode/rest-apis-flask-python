from flask_restx import Resource
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
        return {"message": "Store not found"}, 404

    @classmethod
    def post(cls, name):
        if StoreModel.find_by_name(name):
            return {
                "message": "A store with name '{}' already exists.".format(name)
            }, 400

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted"}, 200
        return {"message": "Store not found"}, 404


class StoreList(Resource):
    @classmethod
    def get(cls):
        return stores_schema.dump(StoreModel.find_all())
