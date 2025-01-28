from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlmodel import Session, select
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.users import User
from utils import engine
# 密碼加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 密碼相關工具
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT Token 工具
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 獲取 Session
def get_session():
    with Session(engine) as session:
        yield session

# 登錄邏輯
def login_user(username: str, password: str, session: Session):
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": create_access_token(data={"sub": user.username}), "token_type": "bearer"}

# 註冊邏輯
def register_user(username: str, email: str, password: str, session: Session):
    # 检查用户是否已经存在
    existing_user = session.exec(select(User).where(User.username == username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")

    # 如果用户不存在，则创建新用户
    hashed_password = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

if __name__ == "__main__":
    session_generator = get_session()
    session = next(session_generator)
    try:
        register_user("admin", "admin@example.com", "password", session)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()
    # 登錄
    try:
        form_data = {"username":"admin", "password":"password"}
        login_user(form_data["username"], form_data["password"], session)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()
