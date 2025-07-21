import sys
import os
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

logger.remove(0)
# logger.add(sys.stderr, format="<m>{time:MMMM D, YYYY > HH:mm:ss zzZ}</m> | {level} | <c>{name}</c>:<c>{file}</c>:<c>{function}</c>:<c>{line}</c> | <b><w>{message}</w></b>")
logger.add(
    sys.stderr, 
    format="<m>{time:DD-MM-YYYY,HH:mm:ss zzZ}</m> | {level} | <c>{file}</c>:<c>{function}</c>:<c>{line}</c> | <b><w>{message}</w></b>",
    level="DEBUG",
    backtrace=True,
    diagnose=True,
)

__all__ = ["logger"]