from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from items import Item, Items
from security import authenticate, identity
from users import UserRegister

app = Flask(__name__)
app.secret_key = 'sam'
api = Api(app)

jwt = JWT(app,authenticate, identity)

api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
  app.run(port=5000, debug=True)