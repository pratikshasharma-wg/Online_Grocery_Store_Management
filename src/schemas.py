from marshmallow import Schema, fields

class LoginUserSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)

class RegisterUserSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    wallet_status = fields.Int(required=True)

class AddProductSchema(Schema):
    product_name = fields.Str(required=True)
    product_price = fields.Int(required=True)
    product_quantity = fields.Int(required=True)

class OrderSchema(Schema):
    email = fields.Str(required=True)
    product_id = fields.Int(required = True)
    product_quantity = fields.Int(required = True)
    cost = fields.Int(required = True)

class UpdateProductSchema(Schema):
    product_name = fields.Str()
    product_price = fields.Int()
    product_quantity = fields.Int()

class WalletSchema(Schema):
    amount = fields.Int(required = True)