from contextlib import asynccontextmanager
import os
from typing import List, Union
from sqlmodel import SQLModel, Session, Field, create_engine, select
from fastapi import FastAPI

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

# DB_DRIVER = os.getenv("DB_DRIVER", default="postgresql")
# DB_USER = os.getenv("DB_USER", default="postgres")
# DB_PASSWORD = os.getenv("DB_PASSWORD", default="postgres")
# DB_HOST = os.getenv("DB_HOST", default="localhost")
# DB_PORT = os.getenv("DB_PORT", default="5432")
# DB_NAME = os.getenv("DB_NAME", default="public")

DB_DRIVER = os.getenv("DB_DRIVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD",)
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

connection_string = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"CONNECTION STRING: {connection_string}" )

engine = create_engine(connection_string, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero
    
@app.get("/heroes/")
def get_all_hero() -> List[Hero]:
    with Session(engine) as session:
        stmt = select(Hero)
        return session.exec(stmt).all()

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}