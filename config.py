import os

from dotenv import load_dotenv

load_dotenv()


def database_url() -> str:
    db_host: str = os.getenv('POSTGRES_HOST') or 'localhost'
    db_port: int = int(os.getenv('POSTGRES_PORT') or 5432)
    db_user: str = os.getenv('POSTGRES_USERNAME') or 'postgres'
    db_pass: str | None = os.getenv('POSTGRES_PASSWORD')
    db_name: str = os.getenv('POSTGRES_DATABASE') or 'postgres'

    return f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


SQLALCHEMY_DATABASE_URI: str = database_url()
SQLALCHEMY_ECHO = True
