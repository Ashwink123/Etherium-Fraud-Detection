import sys
sys.path.append("../")
from fastapi import status, HTTPException, Depends, APIRouter
from utils import CICD
from sqlalchemy.orm import Session
from pgdb_tables import Model_Status
from pydantic import BaseModel
from database import get_db
import pandas as pd

router = APIRouter(tags=['Training'])
class ModelStatus(BaseModel):
    request : str        

@router.post('/train')
def retrain(request: ModelStatus,db: Session = Depends(get_db)):

    if request.request == 'retrain':

        df = pd.read_sql('SELECT * FROM transactions',db.bind)
        status = CICD(df)
        new_status = Model_Status(**status)
        db.add(new_status)
        db.commit()
        db.refresh(new_status)
        return status
    
    elif request.request == 'status':

        model_status = db.query(Model_Status).order_by(Model_Status.tuned_at.asc()).first()
        return model_status
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
          
