from flask import abort, request
from flask_restx import Resource
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
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
        abort(404, "Tag not found.")

    def post(self, name):
        json_input = request.get_json()
        tag = TagModel.find_by_name(name)
        if not tag:
            tag = TagModel(name=name)

        # Add the item to the tag
        try:
            item = ItemModel.query.get(json_input["item_id"])

            if not item:
                abort(400, "An item with this item_id doesn't exist.")

            tag.items.append(item)
        except (TypeError, KeyError):
            abort(400, "Missing required field 'item_id' in JSON body.")

        try:
            tag.save_to_db()
        except SQLAlchemyError:
            abort(500, "An error occurred while inserting the tag.")

        return tag_schema.dump(tag), 201

    def delete(self, name):
        tag = TagModel.find_by_name(name)
        try:
            json_input = request.get_json(force=True)
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
            abort(
                400,
                "Could not delete tag. Make sure tag is not associated with any items, then try again.",  # noqa: E501
            )
        abort(404, "Tag not found.")
