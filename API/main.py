from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection
from routers import train_model , transaction
from config import redis_settings 

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection( 
    host= redis_settings.database_hostname,
    port = redis_settings.database_port,
    db = redis_settings.db,
    decode_responses= True
)


app.include_router(train_model.router)
app.include_router(transaction.router)

