# import jwt
# import requests
# from flask_login import UserMixin
# from peewee import *

# from app import app

# db = MySQLDatabase( app.config['MYSQL_DB'], user=app.config['MYSQL_USER'], password=app.config['MYSQL_PASSWORD'], host=app.config['MYSQL_HOST'] )

# @app.before_request
# def _db_connect():
#     db.connect()


# @app.teardown_request
# def _db_close(exc):
#     if not db.is_closed():
#         db.close()


# def get_table_name(model):
#     return app.config['MYSQL_TABLE']


# class BaseModel(Model):
#     class Meta:
#         database = db
#         table_function = get_table_name

# '''
# Test model class
#     Fields
#     -------
#         id | name
# '''
# class Test(BaseModel):
#     class Meta:
#         table_name = 'test_table'

#     id = AutoField()
#     name = TextField()


# '''
# User model class
# '''
# class User(UserMixin):
#     def __init__(self, id):
#         self.id = id

#     def __repr__(self):
#         return self.id


# class Auth:
#     def auth_api_call(self, data, endpoint):
#         try:
#             api = app.config['AUTH_API']
#             userobj = requests.post(str(api) + endpoint, data=data).json()
            
#             if 'data' in userobj['response'] and 'error' not in userobj['response']['status']:
#                 if 'token' in userobj['response']['data']:
#                     responseObject = self.__decode_auth_token(userobj['response']['data']['token'])
                    
#                     if 'user' in responseObject:
#                         obj = {'message': userobj['response']['message'], 'account': responseObject['accounts'][0]}
#                         context = {k: v for d in [responseObject['user'], obj] for k, v in d.items()}
#                         return context
#             else:
#                 return {'message': userobj['response']['message'], 'status': 'error'}
#         except Exception as e:
#             return {'message': str(e), 'status': 'error'}


#     def __decode_auth_token(self, auth_token):
#         """
#         Validates the auth token
#         :param auth_token:
#         :return: integer|string
#         """
#         try:
#             JWT_SECRET = app.config['JWT_SECRET']
#             payload = jwt.decode(auth_token, str(JWT_SECRET))
#             return payload
#         except jwt.ExpiredSignatureError:
#             return 'Signature expired. Please log in again.'
#         except jwt.InvalidTokenError:
#             return 'Invalid token. Please log in again.'
