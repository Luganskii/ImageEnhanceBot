import os

from dotenv import load_dotenv

load_dotenv()


SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DATABASE')}"
SQLALCHEMY_ECHO = True
