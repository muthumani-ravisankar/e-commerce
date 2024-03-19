from flask import Blueprint , request, session, jsonify
from flask_jwt_extended import jwt_required
from src.orders.Order import Orders ,customError
from src.roles import Roles
bp= Blueprint("orderapi",__name__,url_prefix="/order")


@bp.route('/create',methods=['GET','POST'])
@jwt_required()
def create():
    if(request.method =='GET'):
        return{
            'message':'Method not found  use POST method'
        },405
    if request.method=='POST':
        if('product_id' in request.form and 'user_id' in request.form and 'quantity' in request.form and 'address' in request.form ):
                pid = request.form['product_id']
                uid = request.form['user_id']
                qty = request.form['quantity']
                add = request.form['address']
                try:
                    result= Orders.createorder(pid,uid,qty,add)
                    return {'result':True,
                            'message':'Order created successfully',
                            'Order_id':result['_id'],
                            'User_id':result['user_id'],
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
@Roles.Roles.roles_required(['admin'],message='Access denied: Admin  role required')
def list():
    if(request.method =='POST'):
        return{
            'message':'Method not found  use GET method'
        },405
    #TODO: make Authentication
    if request.method=='GET':
        if(1):
               
                try:
                    result=Orders.listorders()
                    return {'result':True,
                            'message':'Orders are found',
                            'Orders':result,
                            },200
                except customError as e:
                    return {'result':False,
                            'message':str(e)}
    else:
        return{ 'result':False,
                'message':'You are not authenticated'
        },401





@bp.route('/delete/<oid>',methods=['POST','GET'])
@jwt_required()
@Roles.Roles.roles_required(['vendor','admin'],message='Access denied: Admin or Vendor role required')
def delete(oid): 
    #TODO: make authentication   
    if(1):
        if oid:
            try:
                result = Orders.deleteorder(oid)
                return {'result':True,
                    'message':'Order deleted successfully.',
                    'order_id': oid
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
