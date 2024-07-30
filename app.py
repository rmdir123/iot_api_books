from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Depends, Response, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Import models
from database import SessionLocal, engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# https://fastapi.tiangolo.com/tutorial/sql-databases/#crud-utils

@router_v1.get('/books')
async def get_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@router_v1.get('/books/{book_id}')
async def get_book(book_id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

@router_v1.post('/books')
async def create_book(book: dict, response: Response, db: Session = Depends(get_db)):
    # TODO: Add validation
    newbook = models.Book(title=book['title'], author=book['author'], year=book['year'], is_published=book['is_published'], description=book['description'], summary=book['summary'], booktype=book['booktype'])
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    response.status_code = 201
    return newbook

@router_v1.get('/coffee')
async def get_coffee(db: Session = Depends(get_db)):
    return db.query(models.Coffee).all()

@router_v1.get('/coffee/ordercoffee')
async def get_order(db: Session = Depends(get_db)):
    return db.query(models.OrderCoffee).all()

@router_v1.post('/coffee/order')
async def create_order(order_data: dict, response: Response, db: Session = Depends(get_db)):
    # Validate input keys
    required_keys = ["coffee_id", "quantity", "total"]
    if not all(key in order_data for key in required_keys):
        raise HTTPException(status_code=400, detail="Missing required fields")

    # Validate field types
    if not isinstance(order_data["coffee_id"], int) or \
       not isinstance(order_data["quantity"], int) or \
       not isinstance(order_data["total"], int):
        raise HTTPException(status_code=400, detail="Invalid field types")

    # Create a new order
    new_order = models.Order()
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # Create a new order_coffee entry
    new_order_coffee = models.OrderCoffee(
        order_id=new_order.order_id,
        coffee_id=order_data["coffee_id"],  # Use quotes for dictionary keys
        quantity=order_data["quantity"],
        total=order_data["total"],
    )
    
    db.add(new_order_coffee)
    db.commit()
    db.refresh(new_order_coffee)
    
    return {"order": new_order, "order_coffee": new_order_coffee}


app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
