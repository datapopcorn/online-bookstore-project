from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from models.transactions import Transaction
from models.books import Book
from models.users import User
from utils import engine
from services.auth import get_session, SECRET_KEY, ALGORITHM
from jose import jwt, JWTError
from services.auth import login_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def purchase_book(book_asin: str, quantity: int, current_user: User, session: Session):
    # 驗證書籍是否存在
    book = session.exec(select(Book).where(Book.asin == book_asin)).first()
    if not book:
        raise ValueError("Book not found")

    # 計算總金額
    total_amount = book.price * quantity

    # 創建交易記錄
    transaction = Transaction(
        user_id=current_user.email,
        book_id=book_asin,
        quantity=quantity,
        total_amount=total_amount
    )
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction
# 示例用法
if __name__ == "__main__":
    with Session(engine) as session:
        # login to get token
        token = login_user(username="admin", password="password", session=session)
        try:
            current_user = get_current_user(token=token, session=session)
            purchase_book(book_asin="B00TZE87S4", quantity=2, current_user=current_user)
        except ValueError as e:
            print(e)
        except HTTPException as e:
            print(f"HTTP Error: {e.detail}")