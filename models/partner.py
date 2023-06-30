from sqlalchemy import Column, String
from geoalchemy2 import Geometry

from database import Base

class PartnerModel(Base):
    __tablename__ = "partners"

    id = Column(String, primary_key=True, index=True)
    tradingName = Column(String, index=True)
    ownerName = Column(String)
    document = Column(String, unique=True)
    coverageArea = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326))
    address = Column(Geometry(geometry_type='POINT', srid=4326))
