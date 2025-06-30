from fastapi import APIRouter,HTTPException,Header,BackgroundTasks,status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from validation_models.email_validation import sendEmailValidation,verifyEmailValidation
import os
from dotenv import load_dotenv
from db.connection import connectToDB
import random

connection = connectToDB()
cursor = connection.cursor()
load_dotenv()
router = APIRouter(
    prefix='/mail',
    tags=['Email-Sender']
)

email_connection = ConnectionConfig(
    MAIL_USERNAME= os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM= os.environ.get('MAIL_FROM'),
    MAIL_PORT= os.environ.get('MAIL_PORT'),
    MAIL_SERVER= os.environ.get('MAIL_SERVER'),
    MAIL_STARTTLS= os.environ.get('MAIL_STARTTLS'),
    MAIL_SSL_TLS= os.environ.get('MAIL_SSL_TLS'),
    USE_CREDENTIALS= os.environ.get('USE_CREDENTIALS'),
    VALIDATE_CERTS= os.environ.get('VALIDATE_CERTS'),
)

@router.post('')
async def sendEmail(background_tasks:BackgroundTasks,email:sendEmailValidation,SECRET_KEY:str=Header(...)):
    if(SECRET_KEY == os.environ.get('SECRET_KEY')):
        temp_email = 'akshit.22209@knit.ac.in' # REPLACE WITH email.email wherever temp_mail is referenced
        otp = random.randrange(100000,999999)
        cursor.execute(
            '''
                INSERT INTO email_otp(email,otp)
                VALUES(%s,%s)
                ON CONFLICT (email)
                DO UPDATE SET otp = %s
                returning *;
            ''',(temp_email,otp,otp)
        )
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Insertion of otp into table unsuccessful.')
        else:
            connection.commit()
            message = MessageSchema(
                subject="🔐 Your Two-Step Verification Code",
                recipients=[temp_email],
                body=f"""
                <div style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                        <h2 style="color: #333;">Two-Step Verification</h2>
                        <p style="font-size: 16px; color: #555;">Hello,</p>
                        <p style="font-size: 16px; color: #555;">
                            To continue signing in, please use the verification code below:
                        </p>
                        <div style="font-size: 24px; font-weight: bold; color: #1a73e8; margin: 20px 0;">{otp}</div>
                        <p style="font-size: 14px; color: #888;">
                            This code will expire in 10 minutes. If you didn’t request this, please ignore the email.
                        </p>
                        <p style="font-size: 16px; color: #555;">Thank you,<br>Emergency Response Team</p>
                    </div>
                </div>""",
            subtype="html")
        fm = FastMail(email_connection)
        background_tasks.add_task(fm.send_message, message)
        return {"message": "Email has been sent"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')
    
@router.post('/verify')
def verifyOTP(body:verifyEmailValidation,SECRET_KEY:str=Header(...)):
    if SECRET_KEY == os.environ.get('SECRET_KEY'):
        cursor.execute(
            '''
            SELECT otp FROM email_otp
            WHERE email=%s
            ''',(body.email,)
        )
        result = cursor.fetchone()
        if result is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='OTP not generated!')
        else:
            if body.otp == result['otp']:
                return {
                    'status_code':200,
                    'message':'Verified'
                }
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Incorrect OTP')
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Give the valid Secret Key as secret_id')