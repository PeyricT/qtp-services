import string
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
import re
from typing import List, Dict

ensembl_acc_regex = re.compile(
    r'ENSG[0-9]{11}(\.[0-9][0-9]?)?'
)

class EnsemblAC(str):
    
    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = ensembl_acc_regex.fullmatch(v.upper())
        if not m:
            raise ValueError(f"invalid ensembl accession at {v}")
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(f'{v.upper()}')

    def __repr__(self):
        return f'{super().__repr__()}'

def generateUUID():
    return uuid4().hex

class EnsemblDatum(BaseModel):
    id: EnsemblAC
    gene_name : str
    gene_type : str
    version : Optional[int]
    transcript_id : Optional[str]
    protein_id : Optional[str]

class EnsemblCollection(BaseModel):
    comments:str
    content:List[EnsemblAC]