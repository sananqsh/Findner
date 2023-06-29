from sqlalchemy.orm import Session

import models, schemas

def get_partner(db: Session, partner_id: str):
    return db.query(models.Partner).filter(models.Partner.id == partner_id).first()

def get_partner_by_document(db: Session, document: str):
    return db.query(models.Partner).filter(models.Partner.document == document).first()

def create_partner(db: Session, partner: schemas.PartnerCreate):
    db_partner = models.Partner(**partner.dict())
    db.add(db_partner)
    db.commit()
    db.refresh(db_partner)
    return db_partner

def get_partners(db:Session, skip: int = 0, limit: int = 20):
    return db.query(models.Partner).offset(skip).limit(limit).all()
