from fastapi import FastAPI,Header,APIRouter,HTTPException,status
from db.connection import connectToDB
import os
from dotenv import load_dotenv
from validation_models.additional_info import addAdditionalInfoValidation,deleteAdditionalInfoValidation

router = APIRouter(
    prefix='/info'
)
load_dotenv()
connection = connectToDB()
cursor = connection.cursor()

@router.get('/')
def getAdditionalInfo(SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
        '''
            SELECT * FROM additional_info
        ''')
        info_list = cursor.fetchall()
        if info_list is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to fetch info')
        else:
            return {
                'status_code':200,
                'message': 'Fetched Successfully',
                'data': info_list
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')

@router.post('/')
def addAdditionalInfo(body:addAdditionalInfoValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            '''
            INSERT INTO additional_info(name,content)
            VALUES(%s,%s)
            RETURNING *
            ''',(body.name,body.content)
        )
        added_info = cursor.fetchone()
        if added_info is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Unable to add Information')
        else:
            connection.commit()
            return {
                'status_code':201,
                'message':'Record Created!',
                'data': added_info 
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')
    
@router.delete('/')
def deleteAdditionalInfo(body:deleteAdditionalInfoValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY==os.environ.get('SECRET_KEY')):
        cursor.execute('''
            DELETE FROM additional_info
            WHERE id=%s
            RETURNING *
        ''',(body.id,))
        deleted_info = cursor.fetchone()
        if deleted_info is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='No Information associated with this ID')
        else:
            connection.commit()
            return {
                'status_code':200,
                'message':'Record Deleted!',
                'deleted_data':deleted_info
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')