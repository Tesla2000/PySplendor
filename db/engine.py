import os

from sqlalchemy import create_engine

from Config import Config

os.system(
    f"docker run --name {Config.db_name} -e POSTGRES_PASSWORD={Config.db_password} -e POSTGRES_DB={Config.db_name} -d -p 5432:5432 postgres"
)

engine = create_engine(f'postgresql://postgres:{Config.db_password}@localhost:5432/{Config.db_name}', echo=True)
