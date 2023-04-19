from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import train_model , transaction
import uvicorn

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(train_model.router)
app.include_router(transaction.router)


if __name__ == "__main__":
    uvicorn.run(app,host='127.0.0.1',port=8000)
