from pandas import DataFrame, read_csv
from pathlib import Path

class MS_frame():
    def __init__(self, prev=None):
        pass
       # if prev:
       #     self.pd_frame = prev.pd_frame
       #     self.uniprot_key = prev
    @property
    def uniprot_ids(self):
        return self.pd_frame.loc[:, self.uniprot_header].tolist()
    
    def __len__(self):
        return len(self.pd_frame.index)
    
    def parse(self, file:Path, sort_key, data_type, uniprot_key, decimal=","):
        """
        Sort csv file by key
        """
        self.uniprot_header = uniprot_key
        self.sort_key       = sort_key
        df = read_csv(file, sep="\t",  decimal=decimal, dtype = data_type, na_values='#VALEUR!')
        print(set(list(df.keys())))
        if not set([sort_key, uniprot_key]) &  set(list(df.keys())):
            raise KeyError(f"{key} not found in {df.keys()}")
        df = df.dropna().sort_values(by=[sort_key])
        self.pd_frame = df.reset_index(drop=True)
    
    def transform(self, **kwargs):
        df_prev = self.pd_frame
        if 'min_value' in kwargs:
            _ = df_prev.loc[(df_prev[self.sort_key] >= kwargs['min_value'])]
            new_frame = MS_frame()
            new_frame.pd_frame       = _.reset_index(drop=True)
            new_frame.uniprot_header = self.uniprot_header
            new_frame.sort_key       = self.sort_key
            
            return new_frame 

        raise KeyError("unknown transform parameter")
        
