from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Item(Resource):
    TABLE_NAME = 'items'

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            Item.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}

        return item

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {"message": "An error occurred inserting the item."}
        else:
            try:
                Item.update(updated_item)
            except:
                return {"message": "An error occurred updating the item."}
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET price=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'items': items}
