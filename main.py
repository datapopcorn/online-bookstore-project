from fastapi import FastAPI, Depends, Form, HTTPException
from models.users import ensure_database_exists, ensure_schema_exists, create_db_and_tables, User
from services.auth import login_user, register_user, get_session
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from services.transaction import purchase_book, get_current_user

# 初始化 FastAPI 應用
app = FastAPI(
    title="Bookstore API",
    description="API for the Bookstore application",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# 啟動事件：初始化資料庫
@app.on_event("startup")
def startup_event():
    ensure_database_exists()
    for schema in ["auth", "inventory", "sales"]:
        ensure_schema_exists(schema)
    create_db_and_tables()

# 根路由
@app.get("/")
def read_root():
    return {"message": "Welcome to the Bookstore API"}

# 用戶登入路由
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    return login_user(
        username=form_data.username,
        password=form_data.password,
        session=session
    )

# 用戶註冊路由
@app.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session)
):
    return register_user(
        username=username,
        email=email,
        password=password,
        session=session
    )

@app.post("/purchase")
def purchase(
    book_asin: str = Form(...),
    quantity: int = Form(...),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    try:    
        return purchase_book(book_asin=book_asin, quantity=quantity, current_user=current_user, session=session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
# 健康檢查
@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
