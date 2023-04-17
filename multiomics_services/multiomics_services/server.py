from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
from typing import List

from .tools import (
    cover
)

from .schemas import (
    CoverageData
)

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/handshake", response_class=HTMLResponse)
async def handshake(request: Request):
    return 'hello'


@app.post('/cover')
async def get_coverage(coverageData : CoverageData):
    return cover(coverageData.prot_ids, coverageData.gene_ids, coverageData.return_pct)

def start(host, port):
    """Launched with `poetry run start` at root level"""
    uvicorn.run("multiomics_services.server:app", host=host, port=port, reload=True)