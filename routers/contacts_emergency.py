from fastapi import APIRouter,HTTPException,status,Header
from db.connection import connectToDB
from validation_models.contacts_validation import *
import os
from dotenv import load_dotenv

router = APIRouter(
    prefix='/contact',
    tags=['Emergency Contacts']
)

db_connection = connectToDB()
cursor = db_connection.cursor()
load_dotenv()

@router.get('/')
def getEmergencyContacts(SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute('SELECT * FROM emergency_contacts')
        contacts = cursor.fetchall()
        if contacts is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to fetch Emergency Contact')
        else:
            return {
                'status':200,
                'message': 'Successfully Executed',
                'data': contacts
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')

@router.post('/')
def addEmergencyContacts(body:addOrDeleteContactsValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            '''
            INSERT INTO emergency_contacts(name,department,employee_type)
            VALUES (%s,%s,%s)
            returning *
            ''',
        (body.name,body.department,body.employee_type))
        contact = cursor.fetchone()
        if contact is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable To Add Contact')
        else:
            db_connection.commit()
            return {
                'status_code':201,
                'message':'Record Created!',
                'data':contact
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')
    
@router.delete('/')
def deleteEmergencyContact(body:addOrDeleteContactsValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY==os.environ.get('SECRET_KEY')):
        cursor.execute('''
            DELETE FROM emergency_contacts
            WHERE name=%s AND department=%s
            RETURNING *
        ''',(body.name,body.department))
        deleted_contact = cursor.fetchone()
        if deleted_contact is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No Contact found with these credentials')
        else:
            db_connection.commit()
            return {
                'status_code':200,
                'message':'Record Deleted!',
                'deleted_data':deleted_contact
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')