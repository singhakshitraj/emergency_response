from fastapi import FastAPI,status
from routers import emergency_contacts

app = FastAPI()
app.include_router(emergency_contacts.router)

@app.get('/',status_code=status.HTTP_200_OK)
def fxn():
    return {'status_code':200,'message':'rest-api-functioning-properly'}