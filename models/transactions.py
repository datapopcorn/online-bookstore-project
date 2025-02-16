from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from utils import ensure_schema_exists, ensure_database_exists, create_db_and_tables

class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "sales"}
    id: int | None = Field(default=None, primary_key=True)
    user_id: str | None = Field(default=None, foreign_key="auth.users.email")
    book_id: str | None = Field(default=None, foreign_key="inventory.books.asin")
    transaction_date: datetime = Field(default_factory=datetime.now)
    quantity: int
    total_amount: float

if __name__ == "__main__":
    ensure_database_exists()
    ensure_schema_exists(database_schema="sales")
    create_db_and_tables()