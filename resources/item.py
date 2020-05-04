from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


# External representation of entity
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank")

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    @jwt_required()
    def get(self, name):
        """
        Get item by name
        Returns item name and price
        ---
        parameters:
         - in: path
           name: name
           type: string
           required: true
        responses:
          200:
            description: A single item
            schema:
              properties:
                name:
                  type: string
                  description: Name of the item
                price:
                  type: number
                  foramt: double
                  description: Price of the item
          404:
            description: Item does not exist
        """
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred retrieving the item.'}, 500
        if item:
            return item.json()
        return {'message': 'Item does not exist'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": "Item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data) # same as ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error ocurred inserting the item.'}, 500
        return item.json(), 201


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}


    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price'] # add change store_id

        item.save_to_db()

        return item.json(), 200


# External representation of entity
class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

    def delete(self):
        items = ItemModel.query.all()
        for item in items:
            item.delete_from_db()

        return {'message': 'Items deleted'}
