from fastapi import HTTPException,APIRouter,Header,status
from db.connection import connectToDB
from validation_models.device_id_validation import addDeviceIdValidation
import os
from dotenv import load_dotenv
router = APIRouter(
    prefix='/device',
    tags=['Device Management']
)
connection = connectToDB()
cursor = connection.cursor()
load_dotenv()

@router.post('/')
def addDeviceId(body:addDeviceIdValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            ''' 
                INSERT INTO device_details(device_id)
                VALUES(%s)
                returning *
            ''',(body.deviceId,)
        )
        added_data = cursor.fetchone()
        if added_data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to add data!')
        else:
            connection.commit()
            return {
                'status_code':201,
                'message':'Added Successfully!!',
                'data':added_data
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')

@router.get('/delete')
def removeDeviceId():
    try:
        cursor.execute(
        '''
            DELETE FROM device_details
            WHERE time + INTERVAL '8 Hours' <= NOW()
            returning *
        '''
        )
        rec = cursor.fetchall()
        connection.commit()
        return {
        'status_code':200,
        'message':'Deleted Successfully!'
        }
    except Exception as error:
        connection.rollback()
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(error))