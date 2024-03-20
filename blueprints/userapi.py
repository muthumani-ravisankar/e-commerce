
from flask import Blueprint , request, session,jsonify
from flask_jwt_extended import JWTManager,create_access_token, create_refresh_token, jwt_required,  get_jwt_identity,get_jwt
from src.auth.Users import Users, customError
from src.database import database
from src.roles import Roles
bp= Blueprint("userapi",__name__)
db=database.getConnection()
users=db.users


@bp.route('/',methods=['POST','GET'])
@jwt_required()
def test():
    current_user = get_jwt_identity()
    return{
            'user':current_user
        },200
    



@bp.route('/assign_roles', methods=['POST'])
@jwt_required()
@Roles.Roles.roles_required(['admin'],message='Access denied: Admin  role required')
def assign_roles():
    if('username' in request.form and 'roles' in request.form ):
        username = request.form['username']
        new_role = request.form['roles']
        user=users.find_one({"username":username})
        if user is None:
             return{'result':False,
                'message': 'User not found '}, 202
        if new_role!='customer' and new_role!='vendor' and new_role!='admin':
            return{'result':False,
                'message': 'Roles not available, try: vendor,admin,customer '}, 202
        roles = user.get('roles', [])
        has_role = new_role in roles
        if has_role:
            return{'result':False,
                'message': 'Roles Already assigned '}, 202
            
        user['roles'].append(new_role)
        users.update_one({'username': username}, {'$set': {'roles': user['roles']}})
        return {'result':True,
               'message': 'Roles assigned successfully'}, 200



@bp.route('/revoke_roles', methods=['POST'])
@jwt_required()
@Roles.Roles.roles_required(['admin'],message='Access denied: Admin  role required')
def revoke_roles():
    if('username' in request.form and 'roles' in request.form ):
        username = request.form['username']
        role = request.form['roles']
        user=users.find_one({"username":username})
        if user is None:
             return{'result':False,
                'message': 'User not found '}, 202
             
             
        if role!='customer' and role!='vendor' and role!='admin':
            return{'result':False,
                'message': 'Roles not available, try: vendor,admin,customer '}, 202
            
        
        
        roles = user.get('roles', [])
        has_role = role in roles
        if not has_role:
            return{'result':False,
                'message': 'User does not have this role '}, 202
            
            
        users.update_one({'username': username}, {'$set': {'roles': user['roles']}})
        result = users.update_one(
                                {'username': username},
                                {'$pull': {'roles':  role}}
                        )
        if result.modified_count > 0:
            return {'result':True,
               'message': 'Roles revoked successfully'}, 200
        else:
            return {'result':True,
               'message': 'ilefhblelekd'}, 200
           
        
      

   
@bp.route('/signup',methods=['POST','GET'])
def signup():
    if(request.method =='GET'):
        return{
            'message':'Method not found , use POST method'
        },405
    if('username' in request.form and 'email' in request.form and 'password' in request.form):
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            try:
                result= Users.register(username,password,email)
                return {'result':True,'message':'signup success'},200
            except customError as e:
                return {'exception':str(e)}
    else:
        return{
            'message':'Not enough parameterst'
        },400


@bp.route('/login',methods=['POST','GET'])
def login():
    if(request.method == 'GET'):
        return {
            'message':'Method not found , use POST method'
        },405

    if('username' in request.form and 'password' in request.form):
        username = request.form['username']
        password = request.form['password']
        try:
            user = Users.authenticate(username,password)
            if user:
                access_token = create_access_token(identity=username)
                refresh_token = create_refresh_token(identity=username)
                return {'result':True,
                'message':'login success',
                 'tokens':{'access_token':access_token,
                           'refresh_token':refresh_token}}, 200
            else:
                return {'message': 'Invalid username or password'}, 401

            return {
            },200
        except customError as e:
            return{
                'Exception':str(e)
            },400
    else:
        return {
            'message':'Not enough parameters'
        },400
        
        
@bp.route('/users/edit',methods=['POST','GET'])
@jwt_required()
def edituser():
    if(request.method == 'GET'):
        return {
            'message':'Method not found , use POST method'
        },405

    if('username' in request.form and 'mail' in request.form):
        username = request.form['username']
        mail = request.form['mail']
        try:
            user = Users.edituser(username,mail)
            if user:
                return {'result':True,
                'message':'user profile edited successfully',
                 }, 200
            else:
                return {'message': 'Invalid username or password'}, 401
        except customError as e:
            return{
                'Exception':str(e)
            },400
    else:
        return {
            'message':'Not enough parameters'
        },400

logged_out_users = set()
@bp.route('/logout', methods=['POST','GET'])
@jwt_required()
def logout():
    current_user = get_jwt_identity()
    logged_out_users.add(current_user)
    return {'message': 'Successfully logged out'}, 200 

        

@bp.route('/refresh')
@jwt_required(refresh=True)
def refresh():

    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_access_token), 200
    
@bp.route('/users/list')
@jwt_required()
@Roles.Roles.roles_required(['vendor','admin'],message='Access denied: Admin or Vendor role required')
def getusers():
    #TODO: make authentication
    if (1):
        try:
            result =Users.getUsers()
            return result,200
        except customError as e:
            return{
                'Exception':str(e)
            },400
    else:
        return {
            "message":"You are not authenticated"
        },401
    
@bp.route('/changepw',methods=['POST'])
@jwt_required()
def changepassword():
    if(request.method == 'GET'):
        return {
            'message':'Method not found , use POST method'
        },405
    current_user = get_jwt_identity()
    
    if current_user:
        try:
            if("old_password" in request.form and "new_password" in request.form):
                old_pass=request.form["old_password"]
                new_pass=request.form["new_password"]
                Users.changePassword(old_pass,new_pass)
                return {'result':True,
                    "message":"password updated successfully.",
                   
                },200
        except customError as e:
            return{
                'Exception':str(e)
            },400
    else:
        return {"result":False,
            "message":"You are not authenticated"
        },401

