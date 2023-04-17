from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
from typing import List

from .store import EnsemblStore

from .store.schemas import EnsemblAC

class EnsemblRequest(BaseModel) : 
    ensemblIDs : List[EnsemblAC]


class EnsemblFreeRequest(BaseModel) : 
    params : List[str]

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = EnsemblStore()

@app.get("/handshake", response_class=HTMLResponse)
async def handshake(request: Request):
    return 'hello'

@app.get('/ensembl/list')
async def list_genes():
    return store.get_gene_list()

@app.get('/ensembl/length')
async def len_db():
    return {"genes": len(list(store.genes)), "go_terms" : len(list(store.go_terms))}

@app.get('/ensembl/{ensembl_id}')
async def get_gene(ensembl_id: EnsemblAC):
    return store.get_gene(ensembl_id)

@app.post('/ensembls')
async def get_genes(ensembl_request : EnsemblRequest):
    print("get genes", ensembl_request.ensemblIDs)
    return store.get_genes(ensembl_request.ensemblIDs)

@app.post('/ensembls/listids')
async def get_list_ids(ensembl_request: EnsemblFreeRequest):
    print(f"get_gene_ids {len(ensembl_request.params)}")
    return store.get_genes_ids(ensembl_request.params)

@app.post('/collection_scan')
async def get_collection(ensembl_request : EnsemblFreeRequest):
    print(f"get collection for {len(ensembl_request.params)} genes")
    return store.get_collections_from_genes(ensembl_request.params)

def start(host, port):
    """Launched with `poetry run start` at root level"""
    print("test")
    uvicorn.run("ensembl_redis.server:app", host=host, port=port, reload=True)

def load_data(gtf, coll_name:str):
    coll = store.load_ensembl_gtf(gtf)
    print(f"Indexing these entries under collection \"{coll_name}\"")
    store.save_collection(coll_name, coll)

def wipe():
    store.wipe_all()