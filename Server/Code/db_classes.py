from sqlalchemy import Column, Integer, String, ForeignKey, JSON, DateTime, LargeBinary, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import datetime


class Structure(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True)
    creation_date = Column(DateTime, default=datetime.datetime.utcnow)
    folder = Column(String, nullable=False)
    name = Column(String, nullable=False)
    kind = Column(Enum("folder", "file", name="structure_enum"), nullable=False)
    blob_id = Column(Integer, ForeignKey('blobs.id'), nullable=True)
    __table_args__ = (Index('filepath', "folder", "name", unique=True), )
    blobref = relationship("Blob", back_populates="structref")
    
    
class Blob(Base):
    __tablename__ = 'blobs'
    id = Column(Integer, primary_key=True)
    kind = Column(String, nullable=False)
    hashval = Column(String, nullable=True, index=True)
    blob = Column(LargeBinary, nullable=False)
    structref = relationship("Structure", back_populates="blobref")
    