from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt
import pytz
from typing import List
from pydantic import BaseModel, EmailStr

from database import get_db, User, FitnessClass, Booking

# --- CONFIGURATION ---
SECRET_KEY = "SUPER_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
IST = pytz.timezone('Asia/Kolkata')

app = FastAPI(title="Fitness Studio Booking API")

# --- SCHEMAS ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ClassCreate(BaseModel):
    name: str
    dateTime: datetime 
    instructor: str
    availableSlots: int

class BookingRequest(BaseModel):
    class_id: int

# --- AUTH HELPERS ---
def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- API ENDPOINTS ---

# 1. Sign Up
@app.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

# 2. Login
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# 3. Create Class (Protected)
@app.post("/classes")
def create_class(data: ClassCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Ensure time is stored in IST
    ist_time = data.dateTime.astimezone(IST).replace(tzinfo=None)
    
    new_class = FitnessClass(
        name=data.name,
        date_time=ist_time,
        instructor=data.instructor,
        available_slots=data.availableSlots
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

# 4. Get All Classes
@app.get("/classes")
def list_classes(db: Session = Depends(get_db)):
    return db.query(FitnessClass).all()

# 5. Book a Class (Protected + Slot Validation)
@app.post("/book")
def book_class(req: BookingRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # 1. Check if class exists
    target_class = db.query(FitnessClass).filter(FitnessClass.id == req.class_id).first()
    if not target_class:
        raise HTTPException(status_code=404, detail="Class not found")
    
    # 2. Check for available slots
    if target_class.available_slots <= 0:
        raise HTTPException(status_code=400, detail="Class is fully booked")
    
    # 3. Deduct slot and record booking
    target_class.available_slots -= 1
    new_booking = Booking(user_id=current_user.id, class_id=target_class.id)
    
    db.add(new_booking)
    db.commit()
    return {"message": f"Successfully booked {target_class.name} for {current_user.name}"}

# 6. View Own Bookings (Protected)
@app.get("/bookings")
def get_user_bookings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Join classes and bookings to return full class details
    my_bookings = db.query(FitnessClass).join(Booking).filter(Booking.user_id == current_user.id).all()
    return my_bookings