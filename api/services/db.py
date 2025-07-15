from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from api.models.user import Base, User
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./mcp_users.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# Create tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_session_id(db, session_id: str):
    return db.query(User).filter(User.session_id == session_id).first()

def create_or_update_user(db, session_id: str, **kwargs):
    user = get_user_by_session_id(db, session_id)
    if not user:
        user = User(session_id=session_id, **kwargs)
        db.add(user)
    else:
        for key, value in kwargs.items():
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user 