from pydantic import BaseModel
from datetime import date
from typing import Optional


# Схемы для данных угля
class CoalDataBase(BaseModel):
    wp: float
    ap: float
    vg: float
    qlow: int
    k: float
    qbomb: int


class CoalDataCreate(CoalDataBase):
    pass


class CoalData(CoalDataBase):
    date: date

    class Config:
        from_attributes = True


# Схемы для данных работы котла
class BoilerOperationBase(BaseModel):
    boiler_number: int
    d0: int
    o2: float
    t_yx: int
    h_pr: float
    t_cold: int
    g_yn: float


class BoilerOperationCreate(BoilerOperationBase):
    date:date


class BoilerOperation(BoilerOperationBase):
    id: int
    dx: float
    date: date

    class Config:
        from_attributes = True


# Схемы для результатов расчетов
class CalculationResultBase(BaseModel):
    q2: float
    q4: float
    q5: float
    n: float
    b: float
    qist: float
    qpr: float
    bk: float
    bnat: float


class CalculationResultCreate(CalculationResultBase):
    pass


class CalculationResult(CalculationResultBase):
    date: date
    boiler_number: int

    class Config:
        from_attributes = True


# Схема для полного расчета
class FullCalculationRequest(BaseModel):
    date: date
    boiler_number: int