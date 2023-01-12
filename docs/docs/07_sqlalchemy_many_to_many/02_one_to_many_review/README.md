---
title: One-to-many relationships review
description: A super-quick look at creating the Tag model and setting up the one-to-many relationship with Stores.
---

# One-to-many relationship between Tag and Store

Since we've already learned how to set up one-to-many relationships with SQLAlchemy when we looked at Items and Stores, let's go quickly in this section.

## The SQLAlchemy models

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
```

</TabItem>
<TabItem value="store" label="models/store.py">

```python title="models/store.py"
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic")
    # highlight-start
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
    # highlight-end
```

</TabItem>
</Tabs>
</div>

Remember to import the `TagModel` in `models/__init__.py` so that it is then imported by `app.py`. Otherwise SQLAlchemy won't know about it, and it won't be able to create the tables.

## The marshmallow schemas

These are the new schemas we'll add. Note that none of the tag schemas have any notion of "items". We'll add those to the schemas when we construct the many-to-many relationship.

In the `StoreSchema` we add a new list field for the nested `PlainTagSchema`, just as it has with `PlainItemSchema`.

```python title="schemas.py"
class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    # highlight-start
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)
    # highlight-end


class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
```

## The API endpoints

Let's add the Tag endpoints that aren't related to Items:

| Method     | Endpoint              | Description                                             |
| ---------- | --------------------- | ------------------------------------------------------- |
| ✅ `GET`    | `/store/{id}/tag`     | Get a list of tags in a store.                          |
| ✅ `POST`   | `/store/{id}/tag`     | Create a new tag.                                       |
| ❌ `POST`   | `/item/{id}/tag/{id}` | Link an item in a store with a tag from the same store. |
| ❌ `DELETE` | `/item/{id}/tag/{id}` | Unlink a tag from an item.                              |
| ✅ `GET`    | `/tag/{id}`           | Get information about a tag given its unique id.        |
| ❌ `DELETE` | `/tag/{id}`           | Delete a tag, which must have no associated items.      |

Here's the code we need to write to add these endpoints:

```python title="resources/tag.py"
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel
from schemas import TagSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()

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


@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag
```

## Register the Tag blueprint in `app.py`

Finally, we need to remember to import the blueprint and register it!

```python title="app.py"
from flask import Flask
from flask_smorest import Api

import models

from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
# highlight-start
from resources.tag import blp as TagBlueprint
# highlight-end


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    # highlight-start
    api.register_blueprint(TagBlueprint)
    # highlight-end

    return app
```
