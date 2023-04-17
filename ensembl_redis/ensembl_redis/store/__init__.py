from pyrediscore.redantic import RedisStore, KeyStoreError, StoreKeyNotFound
from .schemas import EnsemblDatum, EnsemblCollection, EnsemblAC, EnsemblGeneToId
from pydantic import ValidationError
from sys import stderr
from typing import List
from collections import defaultdict
import time as t

class EnsemblStore():
    def __init__(self, host:str="127.0.0.1", port:int=6379):
        self.base_store = RedisStore(host, port)
        self.base_store.load_model(EnsemblDatum, 'id')
        self.base_store.load_model(EnsemblGeneToId, 'gene_name')
        self.base_store.load_model(EnsemblCollection, 'comments') # to wipe and replace by 
        self.genes = None
        
    def wipe_all(self):
        self.base_store.wipe()

    def load_ensembl_gtf(self, file=None):
        inserted_ok = []
        if file:   
            collection = self.parse_gtf(file)
        else:
            raise ValueError("Please provide gtf source with the file")
            
        for gene in collection:
            try :
                gene_id = gene['gene_id'].split('.')
                obj = EnsemblDatum(
                    id=gene_id[0],
                    gene_type=gene['gene_type'],
                    gene_name=gene['gene_name'],
                    version=gene_id[1] if len(gene_id)>1 else None, 
                    transcript_id=gene['transcript_id'] if 'transcript_id' in gene else None,
                    protein_id=gene['protein_id'] if 'protein_id' in gene else None,
                    )
                genetoid = EnsemblGeneToId(
                    gene_name=gene['gene_name'],
                    gene_id=gene_id[0],
                    gene_version=gene_id[1] if len(gene_id)>1 else None,
                )
            except ValidationError as e:
                print(f"Validation failed for {gene['gene_id']}: {str(e)}", file=stderr)
                continue

            try:
                self.base_store.add(obj)
                self.base_store.add(genetoid)
                #print(prot.id, "added")
            except KeyStoreError:
                #print("Already in db", prot.id)
                pass
            inserted_ok.append(obj.id)
            #print(f"{prot.id} now in db")
        print(f"{len(inserted_ok)} entries added to store")

        return inserted_ok

    def save_collection(self, comments:str, ensembl_ids:List[EnsemblAC]):
        coll = EnsemblCollection(comments=comments, content=ensembl_ids)
        try:
            self.base_store.add(coll)
            #print(coll.comments, "added")
        except KeyStoreError:
            print("Already in db", coll.comments, file=stderr)

    def delete_collection(self, comments:str):
        try:
            self.base_store.delete(comments, model=EnsemblCollection)
        except StoreKeyNotFound:
            print(f"No such collection named {comments}")
            return None
        print(f"Collection \"{comments}\" deleted")
    
    def list_collection(self):
        col_summary = []
        for col_key in self.base_store.list_key(model=EnsemblCollection, skip_prefix=True):
            col_data = self.base_store.get(col_key, EnsemblCollection)
            col_summary.append( (col_data.comments, col_data.content) )
        return col_summary

    def get_gene_collection(self, collection_id_as_comment):
        try:
            collection = self.base_store.get(collection_id_as_comment, EnsemblCollection)
        except StoreKeyNotFound:
            print(f"Collection \"{collection_id_as_comment}\" not found", file=stderr)
            return None
        except KeyError as e:
            print(f"Validation error at key \"{collection_id_as_comment}\": {e}", file=stderr)
        
        for ensembl_id in collection.content:
            try:
                _ = self.get_gene(ensembl_id)
                yield _
            except StoreKeyNotFound:
                print(f"ensembl AC {ensembl_id} not found", file=stderr)
            except KeyError as e:
                print(f"Validation error at key {collection_id_as_comment}: {e}", file=stderr)


    def get_gene(self, ensembl_id):
        try:
            obj = self.base_store.get(ensembl_id)
            return obj
        except StoreKeyNotFound:
            return None
        except KeyError as e:
            print(f"Validation error at key {ensembl_id}: {e}", file=stderr)

    def get_genes(self, ensembl_ids): 
        resp = {}
        for ensembl_id in ensembl_ids:
            resp[ensembl_id] = self.get_gene(ensembl_id)
        return resp
    
    def get_genes_ids(self, genes_names):
        resp = []
        noids = []
        t0 = t.time()
        for gene_name in genes_names:
            try:
                temp_id = self.base_store.get(gene_name, EnsemblGeneToId).gene_id
            except Exception as e:
                noids.append(gene_name)
                temp_id = "NULL"
            resp.append(temp_id)
        
        print(t.time()-t0)
        print(f"not founds gene : {noids}")
        print(f"return {len(resp)} ids")
        return resp

    def get_collections_from_genes(self, ensembl_ids):
        coll_for_genes = {}
        for coll_name, coll_content in self.list_collection():
            coll_for_genes[coll_name] = len(set(coll_content).intersection(set(ensembl_ids)))
            
        return coll_for_genes
        
    def get_gene_list(self):
        if self.genes is None:
            self.genes = self.base_store.get('human_gtf').content
        
        return self.genes

    def parse_gtf(self, file):
        collection = []
        gtf_file = open(file, 'r')

        for line in gtf_file:
            if line.startswith('##'):
                continue

            split_data = line.split('\t')

            if split_data[2] != 'gene':
                continue
                
            infos = split_data[8].split(';')
            dict_ = {}
            for inf in infos:
                if len(inf) < 3:
                    continue
                inf = inf.strip(' ')
                key, value = inf.split(' ')
                dict_[key] = value.strip('"')
            
            collection.append(dict_)
        
        return collection


        

        