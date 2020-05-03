from flask_restful import Resource, reqparse

from models.user import UserModel


# External representation of entity
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank",
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "Username '{}', already exists".format(data['username'])}, 400

        user = UserModel(**data) # same as UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User registered successfully"}, 200
