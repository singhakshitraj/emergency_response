from fastapi import APIRouter,Header,HTTPException,status
from db.connection import connectToDB
import os
from validation_models.check_user_validation import checkAdminOrUserValidation
from dotenv import load_dotenv
router = APIRouter(
    prefix='/check',
    tags=['Check User']
)

connection = connectToDB()
cursor = connection.cursor()
load_dotenv()

@router.post('/')
def checkUser(body:checkAdminOrUserValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        cursor.execute(
            '''
                SELECT role FROM all_users
                WHERE email=%s
            ''',(body.email,)
        )
        rep = cursor.fetchone()
        if rep is None:
            raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail='No account associated with given email-ID')
        else:
            return {
                'status_code':200,
                'message':'Successfully Fetched',
                'data': rep
            }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')