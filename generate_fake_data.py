import random
from datetime import datetime, timedelta
from sqlmodel import select
from models.users import User
from models.books import Book
from models.transactions import Transaction
from services.auth import get_session

def generate_fake_data():
    session = next(get_session())

    # 取得所有書籍（從已載入的 Postgres 讀取）
    books = session.exec(select(Book)).all()
    if not books:
        print("No books found in the database.")
        return
    
    # 生成 50 個用戶
    try: 
        for i in range(50):
            user = User(
                username=f"user{i}",
                email=f"user{i}@example.com",
                hashed_password="hashed_password_placeholder",  # 假數據
                created_at=datetime.now()
            )
            session.add(user)
        session.commit()
    except Exception as e:
        print(f"Error generating users: {e}")

    session = next(get_session())
    # 取得所有書籍（從已載入的 Postgres 讀取）
    books = session.exec(select(Book)).all()
    if not books:
        print("No books found in the database.")
        return 

    '''
    # 生成 1000 筆交易（RFM 模型）
    users = session.exec(select(User)).all()
    if not users:
        print("No users found in the database.")
        return
    try:
        for _ in range(1000):
            user = random.choice(users)
            book = random.choice(books)
            quantity = random.randint(1, 5)
            total_amount = book.price * quantity if book.price else 0.0
            
            # 產生 RFM 指標所需的購買時間
            purchase_date = datetime.now() - timedelta(days=random.randint(0, 365))
            
            transaction = Transaction(
                user_id=user.email,
                book_id=book.asin,  # 書籍以 ASIN 為主鍵
                quantity=quantity,
                total_amount=total_amount,
                transaction_date=purchase_date
            )
            session.add(transaction)
        session.commit()
    except Exception as e:
        print(f"Error generating transactions: {e}")

    print("Fake data generated successfully!")
    session.close()
    '''

    '''
    # 挑選 5 位高頻用戶，並生成 1000 筆交易
    selected_users_list = ["user1", "user8", "user9", "user15", "user26"]
    users = session.exec(select(User).where(User.username.in_(selected_users_list))).all()
    if not users:
        print("No users found in the database.")
        return
    
    # 挑選 20 本暢銷書
    selected_books_list = ["B00TZE87S4", "B08WCKY8MB", "B09KPS84CJ", "B07S7QPG6J", "B00N6PEQV0", "B000OVLKMM", "B00AEBEQUK", "B0BN5742KY", "B098PXH8CK", "B087D5YQXB", "B00AN2JPNI", "B0B69SQNJY", "B07FZPTDJ3", "B0BN4RB7L9", "B0BNWSS8H3", "B0B3Y8QQ6R", "B004J4X32U", "B0CBL7RV55", "B07JKJCWGY", "B01DCHZE3A"]
    books = session.exec(select(Book).where(Book.asin.in_(selected_books_list))).all()
    if not books:
        print("No books found in the database.")
        return
    try:
        for _ in range(1000):
            user = random.choice(users)
            book = random.choice(books)
            quantity = random.randint(1, 5)
            total_amount = book.price * quantity if book.price else 0.0
            purchase_date = datetime.now() - timedelta(days=random.randint(0, 365))
            transaction = Transaction(
                user_id=user.email,
                book_id=book.asin,  # 書籍以 ASIN 為主鍵
                quantity=quantity,
                total_amount=total_amount,
                transaction_date=purchase_date
            )
            session.add(transaction)
        session.commit()
    except Exception as e:
        print(f"Error generating transactions: {e}")

    print("Fake data generated successfully!")
    session.close()
    '''

if __name__ == "__main__":
    generate_fake_data()