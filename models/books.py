from sqlmodel import SQLModel, Field, Session
from sqlalchemy import text
from typing import Optional
from datetime import date
from utils import ensure_schema_exists, ensure_database_exists, create_db_and_tables, engine

class Book(SQLModel, table=True):
    __tablename__ = "books"
    __table_args__ = {"schema": "inventory"}
    asin: str = Field(primary_key=True)
    title: Optional[str] = None
    author: Optional[str] = None
    sold_by: Optional[str] = None
    img_url: Optional[str] = None
    product_url: Optional[str] = None
    stars: Optional[float] = None
    reviews: Optional[int] = None
    price: Optional[float] = None
    is_kindle_unlimited: Optional[bool] = None
    category_id: Optional[int] = None
    is_best_seller: Optional[bool] = None
    is_editors_pick: Optional[bool] = None
    is_good_reads_choice: Optional[bool] = None
    published_date: Optional[date] = None
    category_name: Optional[str] = None

if __name__ == "__main__":
    ensure_database_exists()
    ensure_schema_exists(database_schema="inventory")
    create_db_and_tables()
    # copy kindle_data-v2.csv to table inventory.books
    with Session(engine) as session:
        session.execute(text("COPY inventory.books FROM '/opt/kindle_data-v2.csv' WITH (FORMAT CSV, HEADER true)"))
        session.commit()    