from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///lab6.db')
maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(maker)


# The Base is the class that will be used to create Models
# The SQLAlchemy ORM Models will extend this class
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # Import all the classes that will be used to create ORM Models
    import workspace.models
    Base.metadata.create_all(bind=engine)