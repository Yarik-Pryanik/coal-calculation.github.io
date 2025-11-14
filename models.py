from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class CoalData(Base):
    __tablename__ = "coal_data"
    __table_args__ = {'extend_existing': True}

    date = Column(Date, primary_key=True, index=False)
    wp = Column(Float, nullable=False)  # Влага рабочая %
    ap = Column(Float, nullable=False)  # Зола рабочая %
    vg = Column(Float, nullable=False)  # Выход летучих в-в %
    qlow = Column(Integer, nullable=False)  # Низшая теплота сгор-я ккал/кг
    k = Column(Float, nullable=False)  # Переводной коэфф-т угля
    qbomb = Column(Integer, nullable=False)  # Горючее по бомбе ккал/кг

class BoilerOperation(Base):
    __tablename__ = "boiler_operations"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False, index=True)
    boiler_number = Column(Integer, nullable=False, index=False)
    d0 = Column(Integer, nullable=False)  # Выработка пара по часам Тн
    dx = Column(Float)  # Выработка пара в сутки (рассчитывается)
    o2 = Column(Float, nullable=False)  # Остаточный кислород %
    t_yx = Column(Integer, nullable=False)  # Температура ух.газов Град
    h_pr = Column(Float, nullable=False)  # Данные по продувке %
    t_cold = Column(Integer, nullable=False)  # Температура хол.воздуха Град
    g_yn = Column(Float, nullable=False)  # Данные по горючему в уносах %

    # Внешний ключ на данные угля
    coal_date = Column(Date, ForeignKey('coal_data.date'))


class CalculationResult(Base):
    __tablename__ = "calculation_results"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False, index=True)
    boiler_number = Column(Integer, nullable=False, index=True)

    # Результаты расчетов
    q2 = Column(Float)  # Потери тепла с уходящими газами
    q4 = Column(Float)  # Потери тепла от механического недожога
    q5 = Column(Float)  # Потери тепла в окружающую среду
    n = Column(Float)  # КПД котла
    b = Column(Float)  # Расход топлива
    qist = Column(Float)  # Полезное тепло
    qpr = Column(Float)  # Тепло продувки
    bk = Column(Float)  # Расход условного топлива
    bnat = Column(Float)  # Расход натурального топлива

    # Внешний ключ
    boiler_operation_id = Column(Integer, ForeignKey('boiler_operations.id'))
