import subprocess

from sqlalchemy import create_engine, text

from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_ECHO

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=SQLALCHEMY_ECHO)

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

subprocess.run(['echo', 'Hello world! We are at \n\r'])
subprocess.run(['ls', '-l'])
