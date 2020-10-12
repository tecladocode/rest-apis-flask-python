from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from werkzeug.security import safe_str_cmp
from security  import authenticate, identity

app = Flask(__name__)             # flask
api = Api(app)                    # flask restful

jwt = JWTManager(app)             # flask jwt extended
app.config['JWT_SECRET_KEY'] = 'jose' # flas & flask jwt extended


items =[]    #  Item List


@app.route('/auth', methods=['POST'])
def auth():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
   
    
    
    if authenticate(username, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401

    

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200




@app.route('/item/<string:name>', methods=['GET'])
@jwt_required
def getItem(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404


@app.route('/item/<string:name>', methods=['POST'])    
def postItem(self,name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}'already exists.".format(name)},400
                    
        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201
    
    
@app.route('/items', methods=['GET'])    
class ItemList():
    def get(self):
        return {'items': items}



if __name__ == '__main__':
    app.run()