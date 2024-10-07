import uvicorn

import logging
from logging.handlers import RotatingFileHandler

from fastapi import FastAPI

from utils import CreateSession

app = FastAPI()

@app.get('/models')
async def getmodels():
    return ""

@app.post('/deploy')
async def deploy():
    return

@app.post('infer')
async def inferencr():
    return


if __name__ == '__main__':
    uvicorn.run('main:app', host="127.0.0.1", port=8001, reload=True)