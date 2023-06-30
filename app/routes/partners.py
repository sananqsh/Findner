from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud_partners
import app.schemas as schemas
from app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Partner, status_code=201)
def create_partner(partner: schemas.PartnerCreate, db: Session = Depends(get_db)):
    if crud_partners.get_partner_by_document(db, document=partner.document):
        raise HTTPException(status_code=400, detail="Document already registered")
    
    if crud_partners.get_partner(db, partner_id=partner.id):
        raise HTTPException(status_code=400, detail="id already exists")

    return crud_partners.create_partner(db=db, partner=partner)

@router.get("/", response_model=list[schemas.Partner])
def read_partners(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    partners = crud_partners.get_partners(db, skip=skip, limit=limit)
    return partners

@router.get("/nearest", response_model=schemas.Partner)
def read_nearest_partner(long: float, lat: float, db: Session = Depends(get_db)):
    nearest_partner = crud_partners.get_nearest_partner(db, long=long, lat=lat)
    
    if not nearest_partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    return nearest_partner
