"""multiomics_services ressources microservice

Usage:
  multiomics_services service start [--rh=<redis_host> --rp=<redis_port>] [--port=<portNumber>]
    
Options:
  -h --help     Show this screen.
  --port=<portNumber>  port for public API [default: 2333]
  --rh=<redis_host>  redis DB http adress [default: localhost]
  --as=<collection_name>  assign a name to the inserted collection [default: basename of the xml file]
  --silent  verbosity
  
"""
from docopt import docopt
from .server import start as uvicorn_start
from os.path import basename

args = docopt(__doc__)

if args["start"]:
    print('start')
    uvicorn_start(args['--rh'], int(args['--port']))