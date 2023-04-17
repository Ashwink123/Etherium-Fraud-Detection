from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel





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
    host= 'localhost',
    port = 6379,
    db = 1,
    decode_responses= True
)

class Demo(HashModel):
    name: str
    age: int
    class Meta:
        database: redis




@app.post('/stream')
def write_stream(demo: Demo):
    redis.xadd('demo_stream',demo.dict(),'*')
    return {'Message':'Data Succesfully Written to stream'}


@app.get('/get_data')
def read_stream():
    read_data = redis.xrevrange('demo_stream',max='+',min='-',count=5)     
    return read_data
