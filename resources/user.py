from flask_restful import Resource,reqparse
from models.user import UserModel
from bcrypt_hash import bcrypt
from flask_jwt_extended import jwt_required,create_access_token,create_refresh_token
class RegisterUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="username can not be empty!"
        )
    parser.add_argument('password',
            type=str,
            required=True,
            help="password can not be empty!"
        )
    parser.add_argument('is_admin',
            type=bool,
            required=True,
            help="Please provided the type of user, ADMIN True/False"
        )
    
    @classmethod
    def post(cls):

        data = cls.parser.parse_args()
        if not data:
            return {'msg' : 'Bad Request!'} , 402
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        user = UserModel(username=data['username'],
                         password=bcrypt.generate_password_hash(data['username']),
                         is_admin=data['is_admin'])
        user.save_to_db()
        return {"message": "User created successfully."}, 200



class LoginUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
            type=str,
            required=True,
            help="username can not be empty!"
        )
    parser.add_argument('password',
            type=str,
            required=True,
            help="password can not be empty!")

    
    @classmethod
    def post(cls):

        data = cls.parser.parse_args()
        if not data:
            return {'msg' : 'Bad Request!'} , 402

        user = UserModel.find_by_username(data['username'])
        if not user:
                return {"message": "A user with that username does not exist"}, 400
        if bcrypt.check_password_hash(user.password, data['password']):
            #Lets create the json token
            access_token = create_access_token(identity=user.username,fresh=True)
            secret_token = create_refresh_token(user.username)

            return {"access_token": access_token,"refresh_token" : secret_token}, 200

        return {"message": "Wrong username or password!"}, 401



class UserDetails(Resource):
    @jwt_required
    def get(self):
        users = UserModel.query.all()
        return [user.toJSON() for user in users]

     
