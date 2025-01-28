import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlmodel import create_engine, SQLModel

# 修正 DSN
DATABASE_NAME = "bookstore_db"
DATABASE_URL = "postgresql://postgres:postgres@localhost:5430/bookstore_db"
POSTGRES_URL = "postgresql://postgres:postgres@localhost:5430/postgres"

# 初始化資料庫引擎
engine = create_engine(DATABASE_URL)

# 確保資料庫存在
def ensure_database_exists():
    try:
        conn = psycopg2.connect(POSTGRES_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}';")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute(f"CREATE DATABASE {DATABASE_NAME};")
            print(f"Database '{DATABASE_NAME}' created successfully.")
        else:
            print(f"Database '{DATABASE_NAME}' already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error checking or creating database: {e}")

# 確保 Schema 存在
def ensure_schema_exists(database_schema):
    try:
        conn = psycopg2.connect(
            dbname=DATABASE_NAME,
            user="postgres",
            password="postgres",
            host="localhost",
            port="5430"   
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {database_schema};")
        print(f"Schema '{database_schema}' ensured.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error checking or creating schema: {e}")

# 創建資料表
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)