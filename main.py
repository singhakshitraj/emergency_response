from fastapi import FastAPI,status,Header,HTTPException
from routers import contacts_emergency,additional_info,emergency,check_user_admin,device_info,send_email,admin_panel
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
app.include_router(device_info.router)
app.include_router(send_email.router)
app.include_router(admin_panel.router)
@app.get('/',status_code=status.HTTP_200_OK,tags=['Health Check'])
def healthCheck():
    return {'status_code':200,'message':'rest-api-functioning-properly'}