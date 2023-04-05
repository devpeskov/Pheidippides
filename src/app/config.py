from os import getenv
from os.path import dirname, join

from dotenv import load_dotenv  # type: ignore

load_dotenv(join(dirname(__file__), "../.env"))

TOKEN = getenv("TOKEN")
REDIS_URL = getenv("REDIS_URL")
REDIS_PORT = getenv("REDIS_PORT")
