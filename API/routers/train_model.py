import sys
sys.path.append("../")
from fastapi import Response, status, HTTPException, Depends, APIRouter
from utils import CICD
from request_models import ModelStatus

router = APIRouter(tags=['Training'])


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
          
