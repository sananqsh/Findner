from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from shapely.geometry import shape

from sqlalchemy.orm import Session

import models, schemas
from serializers import PartnerSerializer

def get_partner(db: Session, partner_id: str):
    db_partner = db.query(models.Partner).filter(models.Partner.id == partner_id).first()
    return PartnerSerializer.serialize(db_partner)

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
    db_partners = db.query(models.Partner).offset(skip).limit(limit).all()
    results = []
    for db_partner in db_partners:
        results.append(PartnerSerializer.serialize(db_partner))

    return results
