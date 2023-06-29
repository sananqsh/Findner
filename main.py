from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/partners/", response_model=schemas.PartnerResponse)
def create_partner(partner: schemas.PartnerCreate, db: Session = Depends(get_db)):
    db_partner = crud.get_partner_by_document(db, document=partner.document)
    if db_partner:
        raise HTTPException(status_code=400, detail="Document already registered")
    return crud.create_partner(db=db, partner=partner)

@app.get("/partners/", response_model=list[schemas.PartnerResponse])
def read_partners(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    partners = crud.get_partners(db, skip=skip, limit=limit)
    return partners
