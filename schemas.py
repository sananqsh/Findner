from pydantic import BaseModel
from typing import List

class GeoJSONPoint(BaseModel):
    type: str
    coordinates: List[float]

class GeoJSONMultiPolygon(BaseModel):
    type: str
    coordinates: List[List[List[List[float]]]]

class PartnerBase(BaseModel):
    id: str
    tradingName: str
    ownerName: str
    document: str
    coverageArea: GeoJSONMultiPolygon
    address: GeoJSONPoint

class PartnerCreate(PartnerBase):
    pass

class Partner(PartnerBase):
    class Config:
        orm_mode = True

class PartnerResponse(BaseModel):
    id: str
    tradingName: str
    ownerName: str
    document: str
    coverageArea: str
    address: str

    class Config:
        orm_mode = True
