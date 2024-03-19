from flask import Flask, request, Response , session,jsonify
from src.database import database
import uuid
from time import time
from random import randint
db = database.getConnection()
orders = db.orders

class customError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Orders:
    
    @staticmethod
    def listorders():
        products=list(orders.find({}))
        if products:
            return products
        else:
            raise customError("No Orders found")
    

    @staticmethod
    def createorder(product_id,user_id,quantity,address):
                order_id = str(uuid.uuid4())
               
                _id = orders.insert_one({
                        "_id":order_id,
                        "product_id":product_id,
                        "user_id":user_id,
                        "quantity":quantity,
                        "adress":address     
                    }) 
                inserted_data = orders.find_one({"_id": order_id})
                if(inserted_data): 
                    return inserted_data
                else:
                    raise customError('Error on creating order')
                
    
    
    @staticmethod
    def deleteorder(o_id):
        pdt=orders.find_one({"_id":o_id})
        if(pdt):
                result=orders.delete_one({"_id": o_id})
                if result.deleted_count > 0:
                             return o_id
                else:
                      raise customError("order not found ")
        else:
             raise customError("order id: {} does not exist".format(o_id)) 

       
                   
                    
   