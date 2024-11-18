from .db import SessionLocal


async def get_db():
    """Function-generator for connecting to the database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
