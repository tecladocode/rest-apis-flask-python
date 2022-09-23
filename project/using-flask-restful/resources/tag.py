from flask_restful import Resource, reqparse
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import SQLAlchemyError
from models import TagModel
from models import ItemModel


class Tag(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "item_id",
        type=int,
        required=True,
        help="To create or add a tag to an item, please provide the item_id.",
    )

    def get(self, name):
        tag = TagModel.find_by_name(name)
        if tag:
            return tag.json()
        return {"message": "Tag not found"}, 404

    def post(self, name):
        tag = TagModel.find_by_name(name)
        if not tag:
            tag = TagModel(name=name)

        # Add the item to the tag
        data = self.parser.parse_args()
        item = ItemModel.query.get(data["item_id"])

        if not item:
            return {"message": "An item with this item_id doesn't exist."}, 400

        tag.items.append(item)

        try:
            tag.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred while inserting the tag."}, 500

        return tag.json(), 201

    def delete(self, name):
        tag = TagModel.find_by_name(name)
        try:
            data = self.parser.parse_args()
            if "item_id" in data:
                item = ItemModel.query.get(data["item_id"])
                tag.items.remove(item)
                return {
                    "message": "Item removed from tag",
                    "item": item.json(),
                    "tag": tag.json(),
                }
        except BadRequest:
            # Assume no item_id was passed. Instead delete entire tag.
            # First check tag has no items
            if not tag.items:
                tag.delete_from_db()
                return {"message": "Tag deleted."}
            return {
                "message": "Could not delete tag. Make sure tag is not associated with any items, then try again."
            }
        return {"message": "Tag not found."}, 404
