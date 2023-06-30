from sqlalchemy import func
from geoalchemy2.elements import WKTElement
from shapely.geometry import shape

from sqlalchemy.orm import Session

import schemas
from models.partner import PartnerModel

def get_partner(db: Session, partner_id: str):
    result = query_partners(db).filter(PartnerModel.id == partner_id).first()
    return convert_to_pydantic_model(result)

def get_partner_by_document(db: Session, document: str):
    result = query_partners(db).filter(PartnerModel.document == document).first()
    if result:
        return convert_to_pydantic_model(result)

def create_partner(db: Session, partner: schemas.PartnerCreate):
    # Convert coverageArea to WKT
    coverage_area = shape(partner.coverageArea.dict())
    coverage_area_wkt = WKTElement(coverage_area.wkt, srid=4326)

    # Convert address to WKT
    address = shape(partner.address.dict())
    address_wkt = WKTElement(address.wkt, srid=4326)

    db_partner = PartnerModel(
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

    result = query_partners(db).filter(PartnerModel.id == db_partner.id).first()
    return convert_to_pydantic_model(result)

def get_partners(db:Session, skip: int = 0, limit: int = 20):
    results = query_partners(db).offset(skip).limit(limit).all()

    partners = []
    for partner in results:
        partners.append(convert_to_pydantic_model(partner))

    return partners


def get_nearest_partner(db: Session, lat: float, long: float):
    # Construct a point based on the provided latitude and longitude
    location_point = func.ST_SetSRID(func.ST_MakePoint(long, lat), 4326)

    # Find the nearest partner whose coverage area includes the location
    nearest_partner = query_partners(db).filter(
        func.ST_Within(location_point, PartnerModel.coverageArea)
    ).order_by(
        func.ST_Distance(PartnerModel.address, location_point)
    ).first()

    return convert_to_pydantic_model(nearest_partner)


def query_partners(db:Session):
    return db.query(
        PartnerModel.id,
        PartnerModel.tradingName,
        PartnerModel.ownerName,
        PartnerModel.document,
        func.ST_AsGeoJSON(PartnerModel.coverageArea).label('coverageArea'),
        func.ST_AsGeoJSON(PartnerModel.address).label('address')
    )

def convert_to_pydantic_model(db_partner):
    if db_partner:
        return schemas.Partner(**db_partner._asdict())
