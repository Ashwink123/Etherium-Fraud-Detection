import sys
sys.path.append("../")
from fastapi import status, APIRouter
from utils import Predict
from typing import List
from redis_om import get_redis_connection
from config import redis_settings 
from redis_om import HashModel
from pydantic import BaseModel

redis = get_redis_connection( 
    host= redis_settings.database_hostname,
    port = redis_settings.redis_database_port,
    db = redis_settings.db,
    decode_responses= True
)

class Transactions_Request(HashModel):
    total_erc20_tnxs : float
    erc20_uniq_rec_addr: float
    erc20_uniq_rec_contract_addr: float
    time_diff: float
    total_ether_balance: float
    max_value_received: float
    avg_val_received: float
    erc20_min_val_rec: float
    unique_received_from_addresses: float
    received_tnx: float
    min_value_received: float
    avg_min_between_received_tnx: float
    avg_min_between_sent_tnx: float
    total_ether_sent: float
    max_val_sent: float
    erc20_total_ether_received: float
    avg_val_sent: float
    sent_tnx: float
    class Meta:
        database: redis


router = APIRouter(tags=['Transaction'])

@router.post('/stream',status_code=status.HTTP_201_CREATED)
def write_stream(transactions: Transactions_Request):
    
    
    predictors = transactions.dict()
    predictors.pop('pk')
    print(predictors)

    flag = Predict(predictors)

    transactions=transactions.dict()
    transactions['Flag'] = flag
    redis.xadd('demo_stream',transactions,'*')

    return {'Transaction Status':'Completed'}

@router.get('/get_data')
def read_stream():

    read_data = redis.xrevrange('demo_stream',max='+',min='-',count=5)     
    return read_data