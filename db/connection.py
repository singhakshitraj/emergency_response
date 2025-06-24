from fastapi import HTTPException,status
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
import os
def connectToDB() -> connection :
    load_dotenv()
    try:
        new_connection = psycopg2.connect(
            database = os.environ.get('DATABASE'),
            user = os.environ.get('USER'),
            password = os.environ.get('PASSWORD'),
            host = os.environ.get('HOST'),
            port = os.environ.get('PORT'),
            sslmode="require",
            cursor_factory=RealDictCursor
        )
        return new_connection
    except:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,detail='Unable to connect to database')