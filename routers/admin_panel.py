from fastapi import APIRouter,Header,HTTPException,status
from db.connection import connectToDB
import os
from dotenv import load_dotenv
from validation_models.admin_panel_validation import createUserValidation,deleteUser
load_dotenv()
router = APIRouter(
    prefix='/admin',
    tags=['User Management']
)
connection = connectToDB()
cursor = connection.cursor()

@router.get('/')
def getAllUsers(SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute('select * from all_users')
        data = cursor.fetchall()
        if data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to fetch data!')
        else:
            return {
                'status_code':200,
                'data':data
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')
    
@router.post('/',status_code=status.HTTP_201_CREATED)
def addAUser(user:createUserValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            '''
            SELECT * FROM all_users
            WHERE email=%s
            ''',(user.email,)
        )
        existing_user = cursor.fetchone()
        if existing_user is not None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Email associated with existing User')
        cursor.execute(
            '''
                INSERT INTO all_users(email,role,phone_number,bank_number,department,reporting_manager)
                VALUES(%s,%s,%s,%s,%s,%s)
                returning *
            ''',(user.email,user.role,user.phone,user.bank_number,user.department,user.reporting_manager)
        )
        new_user = cursor.fetchone()
        if new_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to create data!')
        else:
            connection.commit()
            return {
                'status_code':201,
                'message':'Created Successfully!',
                'created_user':new_user
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')
    
@router.put('/',status_code=status.HTTP_200_OK)
def editedDetails(user:createUserValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            '''
                UPDATE all_users
                SET bank_number=%s,department=%s,phone_number=%s,reporting_manager=%s
                WHERE email=%s
                returning *
            ''',(user.bank_number,user.department,user.phone,user.reporting_manager,user.email)
        )
        new_user = cursor.fetchone()
        if new_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to Alter data!')
        else:
            connection.commit()
            return {
                'status_code':200,
                'message':'Altered Successfully!',
                'user':new_user
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')
    
@router.delete('/',status_code=status.HTTP_204_NO_CONTENT)
def deleteDetails(user_email:deleteUser,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            '''
                DELETE FROM all_users
                WHERE email=%s
                returning *
            ''',(user_email.email,)
        )
        deleted_user = cursor.fetchone()
        if deleted_user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Data Delete Unsuccessful!')
        else:
            connection.commit()
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')