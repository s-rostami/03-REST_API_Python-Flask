import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be left blank"
    )


    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
          return item
        return {'message': 'item not founs'}, 404

    @classmethod
    def find_by_name(cls,name):

      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      query = "SELECT * FROM items where name=?"
      result = cursor.execute(query, (name,))

      row = result.fetchone()

      if row:
        return {'item': {'name': row[0], 'price': row[1]}}

        # item = next(filter(lambda x: x['name'] == name, items),None)
        # return {'item': item}, 200 if item else 404

    @classmethod
    def insert_by_name(cls,name):

      data = Item.parser.parse_args()
      print('request data is {}.'.format(data))

      item = {'name': name, 'price': data['price']}

      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      query = "INSERT INTO items VALUES (? ,?)"
      cursor.execute(query, (item['name'], item['price']))

      connection.commit()
      connection.close()

      return item

    @classmethod
    def delete_by_name(cls,name):
      
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      query = "DELETE FROM items WHERE name=?"

      cursor.execute(query, (name,))
      connection.commit()
      connection.close()

    @classmethod
    def update_by_name(cls,name):

      data = Item.parser.parse_args()

      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      query = "UPDATE items SET price=? WHERE name=?"

      item = {'name': name, 'price': data['price']}
      cursor.execute(query, (item['price'], item['name']))

      connection.commit()
      connection.close()
      return item
    
    
    
    def post(self, name):
      if Item.find_by_name(name):
        return {'message': "Item exists in the database"}

      item = self.insert_by_name(name)

      return {'message': 'item {} was added'.format(name), 'item': item}, 201


    def delete(self, name):
        try:
          if self.find_by_name(name):
            self.delete_by_name(name)
            return {'message': "item '{}' was deleted.".format(name)}
          else:
            return {'message': "can not find the item '{}' to delete".format(name)},500
        except:
          return {'message': ' there is a problem with deleteing'}

    def put(self,name):
        
        item = self.find_by_name(name)

        if item is None:
            item = Item.insert_by_name(name)
        else:
            item = Item.update_by_name(name)
        
        return item

class Items(Resource):
    def get(self):
      
      connection = sqlite3.connect('data.db')
      cursor = connection.cursor()

      items = []

      query = "SELECT * FROM items"
      result = cursor.execute(query)
      for row in result:
        items.append({'name': row[0], 'price': row[1]})


      return {'items': items}