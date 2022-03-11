from flask import abort, request
from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest
from sqlalchemy.exc import SQLAlchemyError
from models import TagModel
from models import ItemModel

api = Namespace(
    "tags", description="Operations related to tags and their relationship to items."
)

item_id = api.model("ItemId", {"item_id": fields.Integer()})

nested_item = api.inherit(
    "NestedItem",
    item_id,
    {
        "name": fields.String(),
        "price": fields.Float(),
    },
)

nested_tag = api.model(
    "NestedTag",
    {
        "id": fields.Integer(),
        "name": fields.String(),
    },
)

tag_outputs = api.inherit(
    "Tag",
    nested_tag,
    {
        "items": fields.List(fields.Nested(nested_item)),
    },
)


@api.route("/<name>")
class Tag(Resource):
    @api.marshal_with(tag_outputs)
    def get(self, name):
        tag = TagModel.find_by_name(name)
        if tag:
            return tag
        abort(404, "Tag not found.")

    @api.marshal_with(tag_outputs)
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

        return tag, 201

    def delete(self, name):
        tag = TagModel.find_by_name(name)
        if not tag:
            abort(404, "Tag not found.")

        if not tag.items:
            tag.delete_from_db()
            return {"message": f"Tag '{name}' deleted."}
        abort(
            400,
            "Could not delete tag. Make sure tag is not associated with any items, then try again.",  # noqa: E501
        )


@api.route("/<name>/remove")
class RemoveItemFromTag(Resource):
    @api.expect(item_id, validate=True)
    def delete(self, name):
        tag = TagModel.find_by_name(name)
        if not tag:
            abort(404, "Tag not found.")

        try:
            item_id = request.get_json()["item_id"]
            item = ItemModel.query.get(item_id)
            try:
                tag.items.remove(item)
            except ValueError:
                abort(
                    400,
                    f"Could not remove item with id '{item_id}' from tag."
                    "Make sure item is associated with that item.",
                )
            return {"message": f"Item with id '{item_id}' removed from tag."}
        except BadRequest:
            abort(
                400,
                "Could not delete tag. Make sure tag is not associated with any items, then try again.",  # noqa: E501
            )


@api.route("/")
class TagList(Resource):
    @api.marshal_list_with(tag_outputs)
    def get(self):
        return TagModel.find_all()
