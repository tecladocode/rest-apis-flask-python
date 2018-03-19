from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt_claims, fresh_jwt_required
from models.item import ItemModel


"""
The following resources contain endpoints that are protected by jwt,
one may need a valid access token, a valid fresh token or a valid token with authorized privilege 
to access each endpoint, details can be found in the README.md doc.  
"""


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store_id."
                        )

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @fresh_jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'])

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if claims['isAdmin']:
            return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}, 200
        return {'message': 'Admin privilege required'}, 401
