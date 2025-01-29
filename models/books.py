from sqlmodel import SQLModel, Field, Session
from sqlalchemy import text
from typing import Optional
from datetime import date
from utils import ensure_schema_exists, ensure_database_exists, create_db_and_tables, engine

class Book(SQLModel, table=True):
    __tablename__ = "books"
    __table_args__ = {"schema": "inventory"}
    asin: str = Field(primary_key=True)
    title: str = Field(index=True)
    author: str | None = None
    sold_by: str | None = None
    img_url: str | None = None
    product_url: str | None = None
    stars: float | None = None
    reviews: int | None = None
    price: float | None = None
    is_kindle_unlimited: bool | None = None
    category_id: int | None = None
    is_best_seller: bool | None = None
    is_editors_pick: bool | None = None
    is_good_reads_choice: bool | None = None
    published_date: date | None = None
    category_name: str | None = None

if __name__ == "__main__":
    ensure_database_exists()
    ensure_schema_exists(database_schema="inventory")
    create_db_and_tables()
    # copy kindle_data-v2.csv to table inventory.books
    with Session(engine) as session:
        session.execute(text("COPY inventory.books FROM '/opt/kindle_data-v2.csv' WITH (FORMAT CSV, HEADER true)"))
        session.commit()    