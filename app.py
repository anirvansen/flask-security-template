from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from bcrypt_hash import bcrypt
from resources.user import RegisterUser,LoginUser,UserDetails
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@localhost:3306/rest"

api = Api(app)


jwt = JWTManager(app)

@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(RegisterUser,'/register')
api.add_resource(LoginUser,'/login')
api.add_resource(UserDetails,'/users')



if __name__ == "__main__":
    db.init_app(app)
    bcrypt.init_app(app)
    app.run(port=5400,debug=True)