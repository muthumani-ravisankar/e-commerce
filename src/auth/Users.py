from flask import Flask, request, Response , session,jsonify
from src.database import database

import bcrypt
import uuid
from time import time
from random import randint
db = database.getConnection()
users = db.users

class customError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Users:
    def welcome(self,name):
        return ("Welcome {} !".format(name))
    

    def generate_user_id():
    # Generate a UUID version 4 (random)
        return str(uuid.uuid4())
    
    
    @staticmethod
    def register(username, password,email):
        # TODO: Avoid duplicate signups
    

        user=users.find_one({"username":username})
        mail=users.find_one({"email":email})
        if(not user ):
            if(not mail):
               
                password = password.encode()
                salt = bcrypt.gensalt() # like a secret key that is embedded into the password for verification purposes while logging in
                password = bcrypt.hashpw(password, salt)    
                user_id = Users.generate_user_id()
                _id = users.insert_one({
                    "_id":user_id,
                    "username": username, # TODO: Make as unique index to avoid duplicate entries
                    "password": password,
                    "email":email,
                    "roles":['customer'],
                    "register_time": time(),    
                }) 
            else:
                raise customError("email {} already exist".format(email)) 

        else:
             raise customError("username {} already exist".format(username)) 
        
        return str(username)
    
    @staticmethod
    def authenticate(username,password):
        result = users.find_one({
            'username':username
        })

        if result:
            password_hash = result['password']
            if(bcrypt.checkpw(password.encode(),password_hash)):
               session['uid']=result['_id']
               return username
            else:
                raise customError('Incorrect password')
        else:
            raise customError("Invalid credential")
        
    
        

    @staticmethod
    def changePassword(old_password,new_password):
        user= users.find_one({"_id":session['uid']})
        if user:
            password_hash= user['password']
            if(bcrypt.checkpw(old_password.encode(),password_hash)):
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                users.update_one(
                    {
                        "_id": session['uid']                        
                    },
                    {
                        "$set": {
                        "password": hashed_password                        
                        }
                    }
                )
            else:
                raise customError("Incorrect old password")
        else:
            raise customError("user not found")


    @staticmethod
    def getUsers():
        u=list(users.find({}))
        for user in u:
            user['password']=str(user['password'])
        if u:
            return jsonify(u)
        else:
            raise customError("No users found")
        
    @staticmethod
    def edituser(username,mail):
        user=users.find_one({'_id':session["uid"]})
        if user:
            if(username!=None and mail != None):
                result=users.update_one(
                    {
                        "_id": session['uid']                        
                    },
                    {
                        "$set": {
                        "username": username,
                        "mail":mail                        
                        }
                    }
                )
                if result.modified_count > 0:
                    return True
            else:
                raise customError("username or mail is invalid.")
        else:
            raise customError("user not found")