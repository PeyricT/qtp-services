from pydantic import BaseModel
from typing import Optional, List, Dict

class CoverageData(BaseModel):
    prot_ids : List[str]
    gene_ids : List[str]
    return_pct : bool