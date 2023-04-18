import sys
sys.path.append("../")
from fastapi import status, APIRouter
from main import redis
from request_models import Transactions
from response_models import Transactions_Response
from utils import Predict
from typing import List

router = APIRouter(tags=['Transaction'])

@router.post('/stream',status_code=status.HTTP_201_CREATED)
def write_stream(transactions: Transactions):
    
    flag = Predict(transactions.dict())
    transactions['Flag'] = flag
    redis.xadd('demo_stream',transactions.dict(),'*')

    return {'Transaction Status':'Completed'}


@router.get('/get_data',response_model=List[Transactions_Response])
def read_stream():
    read_data = redis.xrevrange('demo_stream',max='+',min='-',count=5)     
    return read_data