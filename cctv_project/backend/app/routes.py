from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/sources", tags=["Sources"])

@router.post("", response_model=schemas.SourceResponse, status_code=status.HTTP_201_CREATED)
def create_source(source_in: schemas.SourceCreate, db: Session = Depends(get_db)):
    db_source = models.Source(**source_in.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@router.get("", response_model=List[schemas.SourceResponse])
def get_sources(
    search: Optional[str] = Query(None, description="Поиск по названию или локации"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Source)
    if search:
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                models.Source.name.ilike(search_pattern),
                models.Source.location.ilike(search_pattern)
            )
        )
    return query.order_by(models.Source.id.asc()).all()

@router.get("/{source_id}", response_model=schemas.SourceResponse)
def get_source(source_id: int, db: Session = Depends(get_db)):
    source = db.query(models.Source).filter(models.Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    return source

@router.patch("/{source_id}", response_model=schemas.SourceResponse)
def update_source(
    source_id: int,
    source_in: schemas.SourceUpdate,
    db: Session = Depends(get_db)
):
    source = db.query(models.Source).filter(models.Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")

    update_data = source_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(source, field, value)

    db.commit()
    db.refresh(source)
    return source

@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_source(source_id: int, db: Session = Depends(get_db)):
    source = db.query(models.Source).filter(models.Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Источник не найден")
    db.delete(source)
    db.commit()
    return None