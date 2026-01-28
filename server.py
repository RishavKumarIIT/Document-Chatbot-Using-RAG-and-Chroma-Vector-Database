from main import PrepareData,Ask
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app=FastAPI()

vectorstore=None

class InitRequest(BaseModel):
    path: str

@app.get("/load")
def LoadData(req:InitRequest):
    try:
       global vectorstore
       vectorstore=PrepareData(req.path)
       return {"message":"Successfully Loaded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AskRequest(BaseModel):
    query: str

@app.get("/ask")
def Ask_query(req:AskRequest):
    try:
        print("query ",req.query)
        response=Ask(req.query,vectorstore)
        return {"response":response}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))