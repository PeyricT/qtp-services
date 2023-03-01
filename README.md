# Quantitative Proteomics Service

These packages are in development, and needs to be cloned inside the qtp-services pyproject.toml folder

```
# can be omitted
#git clone -b main git@github.com:MMSB-MOBI/pystringbio.git
git clone -b through_uniprot_redis git@github.com:MMSB-MOBI/unigo.git
```


## Python dependencies
`poetry install`
Should install all services dependencies

## Dataset
Download the qtp-services (test dataset)[https://icloud.ibcp.fr/index.php/s/lbEQTJbLkcuDmG6].
`tar -xjf qtp-services_data_test.tar.bz`

## Start redis-server
Redis is a in-RAM noSQL database, we will used for persistancies of many objects required to buildt.
Download and install [REDIS server](https://redis.io/topics/quickstart). Then run as `redis-server`

## Deploy uniprot service
Whole proteome XML files fetched from uniprot, will be parsed, stored by this service. Later, the servie will supply uniprot objects wherever needed.

### start the service
### populate its uniprot database
* uniprot elements
* uniprot collection

## Deploy GO annotation ressources
### start the service
```sh
poetry run python -m unigo store server start
```
### populate GOannotation ressource database with "go blueprint trees"
The database of blueprint Go tree stores the GO term annotation tree of each *proteome*.
Here, *proteomes* are intended as *collection* of uniprot objects stored in the uniprot database.


## Start the PWAS service
```sh
poetry run python -m unigo pwas server start tree
```
### Test the PWAS service
Explain and change collection name to match the one from the archive ?
```sh
poetry run python -m unigo pwas client test ecoli_k12 100 0.1 > pwas_compute_example.json
```

### Install and run 

Download and isntall [REDIS server](https://redis.io/topics/quickstart). Then run as `redis-server`

#### uniprot storage

```shell
poetry run python -m pyproteinsext service uniprot redis start
```

### unigo store
```shell
poetry run python -m unigo store server redis start
``` 

### pwas service

```shell
poetry run python -m unigo pwas server vector
```

### Add a new specie
1. CLI
```shell
poetry run python -m unigo store cli
connect <unigo_host> <unigo_port>
``` 
2. Command line 
```shell
poetry run python -m unigo store client add <owl ontology> <xml proteome>
```

0/

1/ LOAD A NEW SPECIE

2/ WHICH MS AS DEP ?
    2a/ which redis DB ?

3/ Getting ORA results

