from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def name():
    return {'data':{'name':'Vinay'}}