#!/usr/bin/env python
# coding: utf-8


from Code.generate_db import dburl, create_db
from Code.db_classes import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


create_db(dburl)

# Add root folder
engine = create_engine(dburl)
Session = sessionmaker(bind = engine)
session = Session()
session.add(Structure(folder='', name='', kind = 'folder'))
session.close()


