from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from backend.database import get_db
from backend import models, schemas

router = APIRouter(prefix="/boiler", tags=["boiler"])


@router.post("/", response_model=schemas.BoilerOperation, status_code=status.HTTP_201_CREATED)
def create_or_update_boiler_operation(
        boiler_operation: schemas.BoilerOperationCreate,
        db: Session = Depends(get_db)
):
    """
    Добавление или замена данных о работе котла за определенную дату
    Если данные за эту дату и номер котла уже существуют - они будут заменены на новые
    """
    # Получаем дату из тела запроса
    if not boiler_operation.date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата обязательна для заполнения"
        )

    operation_date = boiler_operation.date

    # Проверяем существование данных об угле
    coal_data = db.query(models.CoalData).filter(models.CoalData.date == operation_date).first()
    if coal_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Данные об угле за дату {operation_date} не найдены"
        )

    # Проверяем существование данных за эту дату и номер котла
    existing_operation = db.query(models.BoilerOperation).filter(
        models.BoilerOperation.date == operation_date,
        models.BoilerOperation.boiler_number == boiler_operation.boiler_number
    ).first()

    # Рассчитываем dx
    dx = boiler_operation.d0 / 24

    if existing_operation:
        # Если данные уже существуют - заменяем их
        for field, value in boiler_operation.dict().items():
            if field != 'date':  # Не перезаписываем дату
                setattr(existing_operation, field, value)
        existing_operation.dx = dx
        existing_operation.coal_date = operation_date

        db.commit()
        db.refresh(existing_operation)
        return existing_operation
    else:
        # Создаем новые данные
        db_boiler = models.BoilerOperation(
            date=operation_date,
            dx=dx,
            coal_date=operation_date,
            boiler_number=boiler_operation.boiler_number,
            d0=boiler_operation.d0,
            o2=boiler_operation.o2,
            t_yx=boiler_operation.t_yx,
            h_pr=boiler_operation.h_pr,
            t_cold=boiler_operation.t_cold,
            g_yn=boiler_operation.g_yn
        )
        db.add(db_boiler)
        db.commit()
        db.refresh(db_boiler)
        return db_boiler



@router.get("/{date}/{boiler_number}", response_model=schemas.BoilerOperation)
def get_boiler_operation(
        date: date,
        boiler_number: int,
        db: Session = Depends(get_db)
):
    """Получение данных о работе котла за определенную дату"""
    boiler_operation = db.query(models.BoilerOperation).filter(
        models.BoilerOperation.date == date,
        models.BoilerOperation.boiler_number == boiler_number
    ).first()

    if boiler_operation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Данные за дату {date} для котла {boiler_number} не найдены"
        )

    return boiler_operation



@router.get("/date/{date}", response_model=schemas.BoilerOperation)
def get_boiler_by_date(
        date: date,
        db: Session = Depends(get_db)
):
    """Получение всех данных о работе котлов за определенную дату"""
    boiler_operation = db.query(models.BoilerOperation).filter(models.BoilerOperation.date == date).first()

    if boiler_operation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Данные за дату {date} для котлов не найдены"
        )

    return boiler_operation