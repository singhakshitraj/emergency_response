from fastapi import FastAPI,status
from routers import contacts_emergency,additional_info,emergency
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
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
@app.get('/',status_code=status.HTTP_200_OK)
def fxn():
    return {'status_code':200,'message':'rest-api-functioning-properly'}