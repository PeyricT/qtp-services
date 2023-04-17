def cover(prots, genes, return_pct=False):
    sprots = set(prots)
    sgenes = set(genes)

    nb_prots = len(sprots - sgenes)
    nb_genes = len(sgenes - sprots)
    nb_common = len(sprots) - nb_prots

    if return_pct:
        nb_prots = nb_prots/len(sprots)
        nb_genes = nb_genes/len(sgenes)
    
    return [nb_prots, nb_common, nb_genes]
