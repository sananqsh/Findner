from pydantic import BaseModel, root_validator
from typing import List

import json

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

class Partner(BaseModel):
    id: str
    tradingName: str
    ownerName: str
    document: str
    coverageArea: dict
    address: dict

    @root_validator(pre=True)
    def parse_geojson_fields(cls, values):
        # Make sure the values exist and are string before trying to convert them
        if "coverageArea" in values and isinstance(values["coverageArea"], str):
            values["coverageArea"] = json.loads(values["coverageArea"])
        if "address" in values and isinstance(values["address"], str):
            values["address"] = json.loads(values["address"])
        return values

    class Config:
        orm_mode = True
