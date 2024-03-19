from flask import Blueprint , request, session, jsonify
from flask_jwt_extended import  jwt_required
from src.product.Product import Product ,customError
from src.roles import Roles
bp= Blueprint("productapi",__name__,url_prefix="/product")

@bp.route('/')
def pdt():
    return{
        'error':"Try /create or  /list"
    }
    

@bp.route('/create',methods=['GET','POST'])
@jwt_required()
@Roles.Roles.roles_required(['vendor','admin'],message='Access denied: Admin or Vendor role required')
def create():
    if(request.method =='GET'):
        return{
            'message':'Method not found  use POST method'
        },405
    if request.method=='POST':
        if('tittle' in request.form and 'description' in request.form and 'price' in request.form and 'stock' in request.form ):
                tittle = request.form['tittle']
                desc = request.form['description']
                price = request.form['price']
                stock = request.form['stock']
                try:
                    result= Product.createProduct(tittle,desc,price,stock)
                    return {'result':True,
                            'message':'Product created successfully',
                            'Product_id':result['_id'],
                            'Product_tittle':result['tittle'],
                            },200
                except customError as e:
                    return {'result':False,
                            'message':str(e)}
        else:
            return{'result':False,
                    'message':'Not enough parameters'
            },400
    else:
        return{ 'result':False,
                'message':'You are not authenticated'
        },401


@bp.route('/update',methods=['GET','POST'])
@jwt_required()
@Roles.Roles.roles_required(['vendor','admin'],message='Access denied: Admin or Vendor role required')
def update():
    if(request.method =='GET'):
        return{
            'message':'Method not found  use POST method'
        },405
    if request.method=='POST':
        if('p_id' in request.form and'tittle' in request.form and 'description' in request.form and 'price' in request.form and 'stock' in request.form ):
                p_id = request.form['p_id']
                tittle = request.form['tittle']
                desc = request.form['description']
                price = request.form['price']
                stock = request.form['stock']
                try:
                    result= Product.updateproduct(p_id,tittle,desc,price,stock)
                    return {'result':True,
                            'message':'Product Updated successfully',
                            'Product_id':p_id,
                            },200
                except customError as e:
                    return {'result':False,
                            'message':str(e)}
        else:
            return{'result':False,
                    'message':'Not enough parameters'
            },400
    else:
        return{ 'result':False,
                'message':'You are not authenticated'
        },401


@bp.route('/list',methods=['GET'])
@jwt_required()
def list():
    if(request.method =='POST'):
        return{
            'message':'Method not found  use GET method'
        },405
    #TODO: make Authentication
    if request.method=='GET':
        if(1):
               
                try:
                    result= Product.listproducts()
                    return {'result':True,
                            'message':'Products are found',
                            'Products':result,
                            },200
                except customError as e:
                    return {'result':False,
                            'message':str(e)}
    else:
        return{ 'result':False,
                'message':'You are not authenticated'
        },401



@bp.route('<id>',methods=['GET'])
@jwt_required()
def retrive(id):
    if(request.method =='POST'):
        return{
            'message':'Method not found  use GET method'
        },405
    #TODO: make Authentication
    if request.method=='GET':
        if(1):
               
                try:
                    result= Product.retriveproduct(id)
                    return {'result':True,
                            'message':'Product found',
                            'Product':result,
                            },200
                except customError as e:
                    return {'result':False,
                            'message':str(e)}
    else:
        return{ 'result':False,
                'message':'You are not authenticated'
        },401
        
        
@bp.route('/delete/<p_id>',methods=['POST','GET'])
@jwt_required()
@Roles.Roles.roles_required(['vendor','admin'],message='Access denied: Admin or Vendor role required')
def delete(p_id): 
    #TODO: make authentication   
    if(1):
        if p_id:
            try:
                result = Product.deleteproduct(p_id)
                return {'result':True,
                    'message':'product deleted successfully.',
                    'product_id': p_id
                },200
            except customError as e:
                return{
                    'Exception':str(e)
                },400
        else:
            return {
                'message':'Not enough parameters'
            },400
    else:
        return {
            'message':'You are not authenticated'
        },401
