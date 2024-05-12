import os

from sqlalchemy import create_engine

from Config import Config

os.system(
    f"docker container start {Config.db_name}"
)

engine = create_engine(Config.db_url)
