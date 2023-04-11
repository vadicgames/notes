from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('name')
parser.add_argument('about')
parser.add_argument('email')
parser.add_argument('hashed_password')
parser.add_argument('created_date', required=True)