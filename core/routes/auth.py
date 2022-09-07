from flask import Blueprint, jsonify, make_response, request, current_app as app, redirect
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import jwt
from datetime import datetime, timedelta
from ..database.db import db
from ..models.user import Useraccount

auth_routes = Blueprint("auth", __name__)

# decorator for checking valid json web tokens and authorize access to certain routes
def token_required(func):
    @wraps(func)
    def decorated():
        token = None

        if "Authorization" in request.headers:
            auth = request.headers["Authorization"]
            # remove 'Bearer' in token
            token = str.replace(str(auth), "Bearer ", "")

        if not token:
            # unauthorized
            return jsonify({"msg": "Token is missing."}), 401
        try:
            user_data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=[
                                   "HS256"])  # get decoded user data
            current_user = Useraccount.query.filter_by(
                username=user_data["username"]).first()
        except:
            return jsonify({"msg": "Invalid token."}), 401  # unauthorized
        return func(current_user)

    return decorated

# Register new user 
@auth_routes.route('/register', methods=['POST'])
@cross_origin(origin='*')
def register():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']

        user = Useraccount.query.filter_by(username=username).first()

        # checks for existing user with the same username
        if user!=None:
            return jsonify({'msg': 'Username already exists!'}), 202

        # hashing user password with hashing method
        password = generate_password_hash(password, method='sha256')

        new_user = Useraccount(username=username, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        # generate token with encoded user data
        token = jwt.encode({
            "username": new_user.username,
            "exp": datetime.utcnow() + timedelta(days=7)
        }, app.config["SECRET_KEY"], algorithm="HS256") 
        
        return jsonify({'msg': 'user successfully registered', 'user':new_user.username, "token":token}), 201
    except:
        return jsonify({'msg': 'registration unsuccessful'}), 400


@auth_routes.route('/login', methods=["POST"])
def login():
    try:
        username = request.json['username']
        password = request.json["password"]
        
        user = Useraccount.query.filter_by(username=username).first()
        if not user:
            return jsonify({"msg": "No such user"}), 401  # unauthorized
        
        if check_password_hash(user.password, password):

        # generate token with encoded user data
           token = jwt.encode({
            "username": user.username,
            "exp": datetime.utcnow() + timedelta(days=7)
        }, app.config["SECRET_KEY"], algorithm="HS256")

        # resource created
           return jsonify({"msg": "Successfully logged in", "token": token}), 201
    except:
        return jsonify({"msg": "Incorrect password"}), 403  # forbidden

# to check registered users
@auth_routes.route('/users', methods=['GET'])
def get_all_users():
    users = Useraccount.query.all()
    result = []  
    for user in users:  
        user_data = {}  
        user_data['id'] = user.id 
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['email'] = user.email
        
        result.append(user_data)  
    return jsonify({'users': result})

#example of a route protected by auth decorator
@auth_routes.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return f'Welcome to your profile, {current_user.username} !'
