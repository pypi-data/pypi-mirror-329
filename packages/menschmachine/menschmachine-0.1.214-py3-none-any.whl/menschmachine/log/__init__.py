import logging
import logging.config
import os
import pathlib
import tempfile

import yaml

__loggers = {}

source_dir = pathlib.Path(__file__).parent.resolve()


def load_logging_yaml(filepath: str = f"{source_dir}/logging.yaml"):
    with open(f'{filepath}', 'rt') as f:
        config = yaml.safe_load(f.read())
        try:
            if "file" in config["handlers"]:
                if not os.path.isdir('/tmp'):
                    config["handlers"]["file"]["filename"] = f"{tempfile.gettempdir()}/menschmachine.log"
            if "debug" in config["handlers"]:
                if not os.path.isdir('/tmp'):
                    config["handlers"]["debug"]["filename"] = f"{tempfile.gettempdir()}/menschmachine-debug.log"
        except:
            pass
        logging.config.dictConfig(config)


def get_logger(name: str = "menschmachine") -> logging.Logger:
    if name not in __loggers:
        logger = logging.getLogger(name)
        __loggers[name] = logger
    return __loggers[name]
