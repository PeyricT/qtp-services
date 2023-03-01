import re
def extract_string(string_alias_in, string_detail_in, uniprot_list):
    """
    Extract from string records aliases and links.details that matches provided uniprot list
    """
    uniprot_re     = r'^[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]([A-Z][A-Z0-9]{2}[0-9]){1,2}$'
    uniprot_id_set = set(uniprot_list)
    string_id_set  = set()
    alias_record  = None 
    with open(string_alias_in, "r") as fp:
        for l in fp:
            if alias_record is None:
                alias_record = l
                continue
            b = l.split("\t")
            if re.match(uniprot_re, b[1]):
                if b[1] in uniprot_id_set:
                    alias_record += l
                    string_id_set.add(b[0])
    
    info_record   = None
    with open(string_detail_in, "r") as fp:
        for l in fp:
            if info_record is None:
                info_record = l
                continue
            b = l.split()
            if (b[0] in string_id_set) & (b[1] in string_id_set):
                info_record += l
    return alias_record, info_record