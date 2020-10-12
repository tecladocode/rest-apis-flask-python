from flask_restful import Resource, Api
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)




app = Flask(__name__)
#app.secret_key = 'jose'
app.config['JWT_SECRET_KEY'] = 'jose'  #

#api = Api(app)
api = JWTManager(app)

#jwt = JWT(app, authenticate, identity)  # / creates endpoint /auth

items =[]

@app.route('/auth', methods=['POST'])
class Item(Resource):
    @jwt_required
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404
    
    def post(self,name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}'already exists.".format(name)},400
            
            
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
class ItemList(Resource):
    def get(self):
        return {'items': items}
    
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')

app.run(port=5000, debug=True)