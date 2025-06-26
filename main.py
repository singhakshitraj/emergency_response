from fastapi import FastAPI,status,Header,HTTPException
from routers import contacts_emergency,additional_info,emergency,check_user_admin
from fastapi.middleware.cors import CORSMiddleware
from db.connection import connectToDB

app = FastAPI()
connection = connectToDB()
cursor = connection.cursor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(contacts_emergency.router)
app.include_router(additional_info.router)
app.include_router(emergency.router)
app.include_router(check_user_admin.router)

@app.get('/',status_code=status.HTTP_200_OK)
def fxn():
    return {'status_code':200,'message':'rest-api-functioning-properly'}

@app.get('/delete')
def deleteUsers():
    try:
        cursor.execute(
        '''
            DELETE FROM users
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
    