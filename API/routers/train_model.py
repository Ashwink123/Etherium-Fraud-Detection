import sys
sys.path.append("../")
from fastapi import Response, status, HTTPException, Depends, APIRouter
from utils import CICD
from pydantic import BaseModel

router = APIRouter(tags=['Training'])
class ModelStatus(BaseModel):
    request : str        

@router.post('/train')
def retrain(request: ModelStatus):
    if request == 'train':
        model_status = CICD()
        return model_status
    elif request == 'status':
        # model_status = 
        return model_status
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
          
