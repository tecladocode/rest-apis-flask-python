from flask.views import MethodView
from flask_smorest import Blueprint, abort
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import SQLAlchemyError
from models import TagModel
from models import ItemModel
from schemas import TagSchema, TagUpdateSchema, TagAndItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/tag/<string:name>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, name):
        tag = TagModel.find_by_name(name)
        if tag:
            return tag
        abort(404, message="Tag not found.")

    @blp.arguments(TagUpdateSchema)
    @blp.response(201, TagSchema)
    def post(self, update_data, name):
        tag = TagModel.find_by_name(name)
        if not tag:
            tag = TagModel(name=name)

        # Add the item to the tag
        try:
            item = ItemModel.query.get(update_data["item_id"])

            if not item:
                abort(400, message="An item with this item_id doesn't exist.")

            tag.items.append(item)
        except (TypeError, KeyError):
            abort(400, message="Missing required field 'item_id' in JSON body.")

        try:
            tag.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.arguments(TagUpdateSchema, required=False)
    @blp.response(200, TagAndItemSchema)
    @blp.alt_response(
        202,
        description="Deletes a tag when it has no items and no item_id is passed in the body.",
        example={"message": "Tag deleted."},
        success=True,
    )
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(
        400, description="Missing item_id in body when tag is associated to items."
    )
    def delete(self, tag_data, name):
        """Deletes a tag.

        If the tag is associated to items, expects an item_id in the JSON body and unlinks the item from the tag.

        If the tag is not associated to any items, then does not expect item_id in the JSON body and deletes the tag entirely.
        """
        tag = TagModel.find_by_name(name)
        if "item_id" in tag_data:
            item = ItemModel.query.get(tag_data["item_id"])
            tag.items.remove(item)
            tag.save_to_db()
            return {
                "message": "Item removed from tag",
                "item": item,
                "tag": tag,
            }
        else:
            # Assume no item_id was passed. Instead delete entire tag.
            # First check tag has no items
            if not tag.items:
                tag.delete_from_db()
                return {"message": "Tag deleted."}
            abort(
                400,
                message="Could not delete tag. Make sure tag is not associated with any items, then try again.",  # noqa: E501
            )
        abort(404, message="Tag not found.")
