from fastapi import FastAPI

catch = FastAPI()


@catch.get('/')
def name():
    return {'data':{'name':'Vinay Kumar'}}