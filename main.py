import subprocess

from sqlalchemy import text

from database.config import engine

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

subprocess.run(['echo', 'Hello world! We are at \n\r'])
subprocess.run(['ls', '-l'])
