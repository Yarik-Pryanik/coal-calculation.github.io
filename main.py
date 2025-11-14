from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers.coal import router as coal_router
from routers.boiler import router as boiler_router
from routers.calculations import router as calculations_router

# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Coal Calculation API",
    description="API для расчета параметров работы котлов на основе данных об угле",
    version="1.0.0"
)

# Добавляем CORS middleware для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(coal_router)
app.include_router(boiler_router)
app.include_router(calculations_router)

@app.get("/")
def read_root():
    return {"message": "Coal Calculation API is running!"}

if __name__ == "__main__":
    import uvicorn
    print("Сервер запускается на http://localhost:8000")
    print("Документация: http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)