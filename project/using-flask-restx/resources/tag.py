from flask import request
from flask_restx import Resource, reqparse
from werkzeug.exceptions import BadRequest
from models import TagModel
from models import ItemModel
from schemas import TagSchema, ItemSchema


tag_schema = TagSchema()
item_schema = ItemSchema()


class Tag(Resource):
    def get(self, name):
        tag = TagModel.find_by_name(name)
        if tag:
            return tag_schema.dump(tag)
        return {"message": "Tag not found"}, 404

    def post(self, name):
        json_input = request.get_json()
        tag = TagModel.find_by_name(name)
        if not tag:
            tag = TagModel(name=name)

        # Add the item to the tag
        try:
            item = ItemModel.query.get(json_input["item_id"])

            if not item:
                return {"message": "An item with this item_id doesn't exist."}, 400

            tag.items.append(item)
        except KeyError:
            return {"message": "Missing required field 'item_id'."}

        try:
            tag.save_to_db()
        except:
            return {"message": "An error occurred while inserting the tag."}, 500

        return tag_schema.dump(tag), 201

    def delete(self, name):
        tag = TagModel.find_by_name(name)
        try:
            json_input = request.get_json()
            if "item_id" in json_input:
                item = ItemModel.query.get(json_input["item_id"])
                tag.items.remove(item)
                return {
                    "message": "Item removed from tag",
                    "item": item_schema.dump(item),
                    "tag": tag_schema.dump(tag),
                }
        except BadRequest:
            # Assume no item_id was passed. Instead delete entire tag.
            # First check tag has no items
            if not tag.items:
                tag.delete_from_db()
                return {"message": "Tag deleted."}
            return {
                "message": "Could not delete tag. Make sure tag is not associated with any items, then try again."  # noqa: E501
            }
        return {"message": "Tag not found."}, 404
