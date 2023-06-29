from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, schemas
from database import get_db, create_tables

create_tables()
app = FastAPI()

@app.post("/partners/", response_model=schemas.Partner, status_code=201)
def create_partner(partner: schemas.PartnerCreate, db: Session = Depends(get_db)):
    db_partner = crud.get_partner_by_document(db, document=partner.document)
    if db_partner:
        raise HTTPException(status_code=400, detail="Document already registered")

    return crud.create_partner(db=db, partner=partner)

@app.get("/partners/", response_model=list[schemas.Partner])
def read_partners(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    partners = crud.get_partners(db, skip=skip, limit=limit)
    return partners

@app.get("/partners/nearest", response_model=schemas.Partner)
def read_nearest_partner(long: float, lat: float, db: Session = Depends(get_db)):
    nearest_partner = crud.get_nearest_partner(db, long=long, lat=lat)
    
    if not nearest_partner:
        raise HTTPException(status_code=404, detail="Partner not found")

    return nearest_partner
