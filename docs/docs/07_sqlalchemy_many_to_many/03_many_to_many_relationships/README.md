---
title: Many-to-many relationships
description: Learn to set up a many-to-many relationship between two models using SQLAlchemy.
---

# Many-to-many relationships

## The SQLAlchemy models

In one-to-many relationships, one of the models has a foreign key that links it to another model. 

However, for a many-to-many relationship, one model can't have a single value as a foreign key (otherwise it would be a one-to-many!). Instead, what we do is construct a **secondary table** that has, in each row, a tag ID and and item ID.

| id  | tag_id | item_id |
| --- | ------ | ------- |
| 1   | 2      | 5       |
| 2   | 1      | 4       |
| 3   | 4      | 5       |
| 4   | 1      | 3       |

<details>
  <summary>Explanation of the table above</summary>
  <div>
    <p>The table above has 4 rows, which tell us the following:</p>
    <ol>
        <li>Tag with ID <code>1</code> is linked to Items with IDs <code>3</code> and <code>4</code>.</li>
        <li>Tag with ID <code>2</code> is linked to Item with ID <code>5</code>.</li>
        <li>Tag with ID <code>4</code> is linked to Item with ID <code>5</code>.</li>
    </ol>
    <p>And therefore:</p>
    <ol>
        <li>Item with ID <code>3</code> is linked to Tag with ID <code>1</code>.</li>
        <li>Item with ID <code>4</code> is linked to Tag with ID <code>1</code>.</li>
        <li>Item with ID <code>5</code> is linked to Tags with IDs <code>2</code> and <code>4</code>.</li>
    </ol>
    <p>This is how many-to-many relationships work, and through this secondary table, the <code>Tag.items</code> and <code>Item.tags</code> attributes will be populated by SQLAlchemy.</p>
  </div>
</details>

The rows in this table then signify a link between a specific tag and a specific item, but without the need for those values to be stored in the tag or item models themselves.

### Writing the secondary table for many-to-many relationships

As we've just seen, many-to-many relationships use a secondary table which stores which models of one side are related to which models of the other side.

Just as we did with `Item`, `Store`, and `Tag`, we'll create a model for this secondary table:

```python title="models/item_tags.py"
from db import db


class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
```

Let's also add this to our `models/__init__.py` file:

```python title="models/__init__.py"
from models.item import ItemModel
from models.tag import TagModel
from models.store import StoreModel
from models.item_tags import ItemsTags
```

### Using the secondary table in the main models


import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<div className="codeTabContainer">
<Tabs>
<TabItem value="tag" label="models/tag.py" default>

```python title="models/tag.py"
from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer(), db.ForeignKey("stores.id"), nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    # highlight-start
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")
    # highlight-end
```

</TabItem>
<TabItem value="item" label="models/item.py">

```python title="models/item.py"
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("StoreModel", back_populates="items")

    # highlight-start
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
    # highlight-end
```

</TabItem>
</Tabs>
</div>

## The marshmallow schemas

Next up, let's add the nested fields to the marshmallow schemas.

The `TagAndItemSchema` will be used to return information about both the Item and Tag that have been modified in an endpoint, together with an informative message.

```python title="schemas.py"
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    # highlight-start
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    # highlight-end

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    # highlight-start
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    # highlight-end
    store = fields.Nested(PlainStoreSchema(), dump_only=True)

# highlight-start
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)
# highlight-end
```

## The API endpoints

Now let's add the rest of our API endpoints (grayed out are the ones we implemented in [one-to-many relationships review](../one_to_many_review/))!

| Method                                         | Endpoint                                                | Description                                                                            |
| ---------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| <span style={{opacity: "50%"}}>✅ `GET`</span>  | <span style={{opacity: "50%"}}>`/store/{id}/tag`</span> | <span style={{opacity: "50%"}}>Get a list of tags in a store.</span>                   |
| <span style={{opacity: "50%"}}>✅ `POST`</span> | <span style={{opacity: "50%"}}>`/store/{id}/tag`</span> | <span style={{opacity: "50%"}}>Create a new tag.</span>                                |
| ✅ `POST`                                       | `/item/{id}/tag/{id}`                                   | Link an item in a store with a tag from the same store.                                |
| ✅ `DELETE`                                     | `/item/{id}/tag/{id}`                                   | Unlink a tag from an item.                                                             |
| <span style={{opacity: "50%"}}>✅ `GET`</span>  | <span style={{opacity: "50%"}}>`/tag/{id}`</span>       | <span style={{opacity: "50%"}}>Get information about a tag given its unique id.</span> |
| ✅ `DELETE`                                     | `/tag/{id}`                                             | Delete a tag, which must have no associated items.                                     |

Here's the code (new lines highlighted):

```python title="resources/tag.py"
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
# highlight-start
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema
# highlight-end

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()  # lazy="dynamic" means 'tags' is a query

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag with that name already exists in that store.")

        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e),
            )

        return tag

# highlight-start
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return tag

    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the tag.")

        return {"message": "Item removed from tag", "item": item, "tag": tag}
# highlight-end


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    # highlight-start
    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it.",
        example={"message": "Tag deleted."},
    )
    @blp.alt_response(404, description="Tag not found.")
    @blp.alt_response(
        400,
        description="Returned if the tag is assigned to one or more items. In this case, the tag is not deleted.",
    )
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )
    # highlight-end
```

And with that, we're done!

## Making sure Store ID matches when linking tags

If you wanted to, you can make sure that you can only link a tag that belongs to a certain store, with an item of that same store.

Something like this would work:

```py
if item.store.id != tag.store.id:
    abort(400, message="Make sure item and tag belong to the same store before linking.")
```

Now we're ready to look at securing API endpoints with user authentication.