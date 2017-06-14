from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Ryan'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth create a new endpoint

items = []

class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        # filter function return a filter object and use list will return list, next will return the first one
        return {'item': item}, 200 if item else 404

    @jwt_required
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {'message': "An item with name '{}' is already exists.".format(name)}, 400 # bad request already have one inside
        data = request.get_json() # use force = True will automatically look into the request content, so user don't have to provide the content-type header
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
