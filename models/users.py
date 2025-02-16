from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from utils import ensure_database_exists, ensure_schema_exists, create_db_and_tables
from datetime import datetime

# SQLModel 模型
class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}  # 設定 Schema 為 auth
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)



if __name__ == "__main__":
    ensure_database_exists()
    ensure_schema_exists(database_schema="auth")
    create_db_and_tables()
