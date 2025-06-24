from fastapi import APIRouter,Header,HTTPException,status
from db.connection import connectToDB
import os
from dotenv import load_dotenv
from validation_models.emergency import addEmergencyValidation,emergencyResolvedValidation

router = APIRouter(
    prefix='/emergency',
    tags=['Emergency']
)
connection = connectToDB()
cursor = connection.cursor()
load_dotenv()

@router.get('/')
def getEmergencyList(SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            '''
                SELECT * FROM emergency
                WHERE time >= NOW() - INTERVAL '2 Days'
            '''
        )
        allEmergencies = cursor.fetchall()
        if allEmergencies is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to fetch all Emergencies')
        else:
            return {
                'status_code':200,
                'message':'Fetched Successfully',
                'data':allEmergencies
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')
    
@router.post('/')
def addEmergency(body:addEmergencyValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            '''
            INSERT INTO emergency(location,type,additional_info)
            VALUES (%s,%s,%s)
            returning *
            ''',
        (body.location,body.type,body.additional_info))
        new_emergency = cursor.fetchone()
        if new_emergency is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable To Create Emergency!')
        else:
            connection.commit()
            return {
                'status_code':201,
                'message':'Record Created!',
                'data':new_emergency
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')
    
@router.patch('/')
def markEmergencyAsResolved(body:emergencyResolvedValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY==os.environ.get('SECRET_KEY')):
        cursor.execute('''
            UPDATE emergency
            SET resolved=%s
            where id=%s
            RETURNING *
        ''',(True,body.id,))
        updated_emergency = cursor.fetchone()
        if updated_emergency is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No Contact found with these credentials')
        else:
            connection.commit()
            return {
                'status_code':200,
                'message':'Record Updated!',
                'deleted_data':updated_emergency
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')