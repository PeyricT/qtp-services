from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, parse, register_namespace # dump
def set_entries(xml_file:Path):
    tree = parse(xml_file)
    root = tree.getroot()
    uri  = "http://uniprot.org/uniprot" 
    register_namespace("",  uri)
    ns = '{' + uri  + '}'
    
    def indexing():
        index = {}
        proteins = root.findall(ns + 'entry')
        for entry in proteins:
            accessions = entry.findall(ns+"accession")
            for acc in accessions:
                index[acc.text] = entry
        return index
    print("indexing")
    p_index = indexing()
    print(f"successfully indexed {len(p_index)}")
    def entry_find(uniprot_id):
        if uniprot_id in p_index:
            return p_index[uniprot_id]
        return None
    new_root = Element(root.tag, attrib=root.attrib)
    new_tree = ElementTree(new_root)
    
    return entry_find, new_tree
    
def transform_xml_tree(xml_file, uniprot_id_list):
    proteome_file = xml_file
    entry_getter, new_tree = set_entries(proteome_file)
    for uniprot_id in uniprot_id_list:
        e = entry_getter(uniprot_id)
        if not e:
            print(f"{uniprot_id} not found")
            continue
        new_tree.getroot().append(e)
    return new_tree