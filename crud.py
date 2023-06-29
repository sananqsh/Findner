from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from shapely.geometry import shape

from sqlalchemy.orm import Session

import models, schemas
from serializers import PartnerSerializer

import json

def get_partner(db: Session, partner_id: str):
    result = query_partners(db).filter(models.Partner.id == partner_id).first()
    
    if result is None:
        return None
    
    # Convert the result to a dictionary and parse 'coverageArea' and 'address' to GeoJSON
    partner_dict = dict(result)
    partner_dict["coverageArea"] = json.loads(partner_dict["coverageArea"])
    partner_dict["address"] = json.loads(partner_dict["address"])

    return partner_dict

def get_partner_by_document(db: Session, document: str):
    db_partner = db.query(models.Partner).filter(models.Partner.document == document).first()
    return PartnerSerializer.serialize(db_partner)

def create_partner(db: Session, partner: schemas.PartnerCreate):
    # Convert coverageArea to WKT
    coverage_area = shape(partner.coverageArea.dict())
    coverage_area_wkt = WKTElement(coverage_area.wkt, srid=4326)

    # Convert address to WKT
    address = shape(partner.address.dict())
    address_wkt = WKTElement(address.wkt, srid=4326)

    db_partner = models.Partner(
        id=partner.id,
        tradingName=partner.tradingName,
        ownerName=partner.ownerName,
        document=partner.document,
        coverageArea=coverage_area_wkt,
        address=address_wkt,
    )

    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)

    return PartnerSerializer.serialize(db_partner)

def get_partners(db:Session, skip: int = 0, limit: int = 20):
    db_partners = query_partners(db).offset(skip).limit(limit).all()

    results = []
    for db_partner in db_partners:
        # Convert the result to a dictionary and parse 'coverageArea' and 'address' to GeoJSON
        partner_dict = dict(db_partner)
        partner_dict["coverageArea"] = json.loads(partner_dict["coverageArea"])
        partner_dict["address"] = json.loads(partner_dict["address"])
        results.append(partner_dict)

    return results

def query_partners(db:Session):
    return db.query(
        models.Partner.id,
        models.Partner.tradingName,
        models.Partner.ownerName,
        models.Partner.document,
        func.ST_AsGeoJSON(models.Partner.coverageArea).label('coverageArea'),
        func.ST_AsGeoJSON(models.Partner.address).label('address')
    )
