import logging
import os

from datetime import datetime

DEFAULT_PROJECT = "controlled-vocabulary-utils"

DEFAULT_TIMESTAMP = str(datetime.today().strftime("%Y-%m-%d-%H%M%S"))

DEFAULT_OUTDIR_BASE = os.path.join(
    "/tmp/",
    os.getenv("USER"),
    DEFAULT_PROJECT,
)

DEFAULT_LOGGING_FORMAT = (
    "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"
)

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = False

# Add this line to define the LRU_CACHE_MAXSIZE constant
LRU_CACHE_MAXSIZE = 128
