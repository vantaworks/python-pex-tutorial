import argparse
import types
from importlib.machinery import SourceFileLoader
import logging
from .web_server import StandaloneApplication
from .web_api import app

logger = logging.getLogger(__name__)

__version__ = 0.1

def config_importer(config_path):
    logger.info("LOGGING TEST FOR A CONFIG FILE")
    omit_config_keys = ["__builtins__", '__doc__', '__loader__',
                        '__name__', '__package__', '__spec__']

    loader = SourceFileLoader("conf", config_path)
    mod = types.ModuleType(loader.name)
    loader.exec_module(mod)
    options = vars(mod)
    for key in omit_config_keys:
        del options[key]
    return options

def launcher(live_reload=False):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')

    arg_parse = argparse.ArgumentParser(description="A super basic Flask + Gunicorn app")
    arg_parse.add_argument("-c", "--config-file", dest="config_file",
                           help="Config File location", default=None)
    args = arg_parse.parse_args()

    if not args.config_file:
        options = {
            'bind': '%s:%s' % ('127.0.0.1', '8080'),
            'workers': 3,
            'reload': live_reload,
        }
    else:
        options = config_importer(args.config_file)
    StandaloneApplication(app, options).run()
