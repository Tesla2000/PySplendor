import os

from sqlalchemy import create_engine

from Config import Config

os.system(
    f"docker container start {Config.db_name}"
)

engine = create_engine(f'postgresql://postgres:{Config.db_password}@localhost:5432/{Config.db_name}', echo=True)
