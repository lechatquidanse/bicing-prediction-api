from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

BICING_API_DB_DATABASE = os.getenv("POSTGRES_DB")
BICING_API_DB_USER = os.getenv("POSTGRES_USER")
BICING_API_DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
BICING_API_DB_HOST = os.getenv("POSTGRES_HOST")
BICING_API_DB_PORT = os.getenv("POSTGRES_PORT")

PERSISTENCE_MODEL_FILE_SYSTEM_PATH = os.getenv('PERSISTENCE_MODEL_FILE_SYSTEM_PATH')
