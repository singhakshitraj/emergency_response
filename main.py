from fastapi import FastAPI,status
from routers import contacts_emergency,additional_info,emergency

app = FastAPI()
app.include_router(contacts_emergency.router)
app.include_router(additional_info.router)
app.include_router(emergency.router)
@app.get('/',status_code=status.HTTP_200_OK)
def fxn():
    return {'status_code':200,'message':'rest-api-functioning-properly'}