from flask_restful import Resource, reqparse
from auth_api.models.item import ItemModel
from auth_api.security import require_appkey, mustbe_admin


class Item(Resource):
    method_decorators = [mustbe_admin, require_appkey]

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is required")  # parse the json and add specifications

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item with name "{}" already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item"}, 500

        return item.json(), 201

    def put(self, name):  # Update existing or create
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


class ItemList(Resource):
    method_decorators = [require_appkey]

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
