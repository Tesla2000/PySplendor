import atexit

from sqlalchemy.orm import sessionmaker

from db.engine import engine

Session = sessionmaker(bind=engine)
session = Session()


@atexit.register
def close_connection():
    session.commit()
    session.close()
