from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from shapely.geometry import shape

from sqlalchemy.orm import Session

import models, schemas

def get_partner(db: Session, partner_id: str):
    result = query_partners(db).filter(models.Partner.id == partner_id).first()
    return convert_to_pydantic_model(result)

def get_partner_by_document(db: Session, document: str):
    result = query_partners(db).filter(models.Partner.document == document).first()
    if result:
        return convert_to_pydantic_model(result)

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

    result = query_partners(db).filter(models.Partner.id == db_partner.id).first()
    return convert_to_pydantic_model(result)

def get_partners(db:Session, skip: int = 0, limit: int = 20):
    results = query_partners(db).offset(skip).limit(limit).all()

    partners = []
    for partner in results:
        partners.append(convert_to_pydantic_model(partner))

    return partners

def query_partners(db:Session):
    return db.query(
        models.Partner.id,
        models.Partner.tradingName,
        models.Partner.ownerName,
        models.Partner.document,
        func.ST_AsGeoJSON(models.Partner.coverageArea).label('coverageArea'),
        func.ST_AsGeoJSON(models.Partner.address).label('address')
    )

def convert_to_pydantic_model(db_partner):
    return schemas.Partner(**dict(db_partner))
