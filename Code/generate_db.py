import urllib.parse, os
from Code.db_classes import Base
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

storage_name = os.environ.get("storage_name")
storage_host = os.environ.get("storage_host")
storage_pass = os.environ.get("storage_pass")
storage_user = os.environ.get("storage_user")

storage_name_quoted = urllib.parse.quote_plus(storage_name)
storage_host_quoted = urllib.parse.quote_plus(storage_host)
storage_pass_quoted = urllib.parse.quote_plus(storage_pass)
storage_user_quoted = urllib.parse.quote_plus(storage_user)

dburl = "postgresql://{user}:{pwd}@{host}/{name}".format(name= storage_name_quoted, 
                                                          host= storage_host_quoted, 
                                                          pwd= storage_pass_quoted, 
                                                          user= storage_user_quoted)

def create_db(dburl):
    engine = create_engine(dburl, echo = True)

    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)