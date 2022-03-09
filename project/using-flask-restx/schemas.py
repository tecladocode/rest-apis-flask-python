from marshmallow import Schema, fields


class ItemSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int(load_only=True)
    store = fields.Nested(lambda: StoreSchema(exclude=("items",)), dump_only=True)
    tags = fields.List(
        fields.Nested(lambda: TagSchema(exclude=("items",))), dump_only=True
    )


class StoreSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    items = fields.List(fields.Nested(ItemSchema(exclude=("store",))), dump_only=True)


class TagSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    items = fields.List(fields.Nested(ItemSchema(exclude=("tags",))), dump_only=True)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str(load_only=True)
