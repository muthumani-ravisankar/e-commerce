from flask import Flask, request, Response , session,jsonify
from src.database import database
import uuid
from time import time
from random import randint
db = database.getConnection()
product = db.products

class customError(Exception):
    def __init__(self, message):
        super().__init__(message)

class Product:
    
    @staticmethod
    def listproducts():
        products=list(product.find({}))
        if products:
            return products
        else:
            raise customError("No Products found")
    
    @staticmethod
    def retriveproduct(id):
        pdt=product.find_one({"_id":id})
        if pdt:
            return pdt
        else:
            raise customError("Product id is invalid ")


    @staticmethod
    def createProduct(product_tittle, product_desc,product_price,product_stock):
                product_id = str(uuid.uuid4())
               
                _id = product.insert_one({
                        "_id":product_id,
                        "tittle":product_tittle,
                        "desc":product_desc,
                        "price":product_price,
                        "stock":product_stock     
                    }) 
                inserted_data = product.find_one({"_id": product_id})
                if(inserted_data): 
                    return inserted_data
                else:
                    raise customError('Error on creating product')
                
    
    @staticmethod
    def updateproduct(product_id,product_tittle, product_desc,product_price,product_stock):
        pdt=product.find_one({"_id":product_id})
        if pdt:
            result=product.update_one(
            {
                "_id": product_id,
            },
            {
                "$set": {
                "tittle": product_tittle,
                "desc":product_desc,
                "price":product_price,
                "stock":product_stock,
                "updated_at": time()
                }
            }
            )
            return result
            

        else:
            raise customError("product id: {} does not exist".format(product_id))
        
    
    @staticmethod
    def deleteproduct(p_id):
        pdt=product.find_one({"_id":p_id})
        if(pdt):
                result=product.delete_one({"_id": p_id})
                if result.deleted_count > 0:
                             return p_id
                else:
                      raise customError("Blog not found ")
        else:
             raise customError("product id: {} does not exist".format(p_id)) 

       
                   
                    
   