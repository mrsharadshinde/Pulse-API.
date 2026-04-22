import logging
import sys

# 1. Create a custom logger
logger = logging.getLogger("pulse_api")
logger.setLevel(logging.INFO)

# 2. Define the exact format of the log messages
formatter = logging.Formatter(
    fmt= "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 3 create file handler that saves logs to permanent files
file_handler = logging.FileHandler("pulse.log", encoding="utf-8")
file_handler.setFormatter(formatter)

# 4. Create a Stream Handler (Still prints to your terminal while developing)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# 5. Add both handlers to our logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)