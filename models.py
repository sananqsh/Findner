from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

from database import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(String, primary_key=True, index=True)
    tradingName = Column(String, index=True)
    ownerName = Column(String)
    document = Column(String, unique=True)
    coverageArea = Column(JSONB)
    address = Column(JSONB)
