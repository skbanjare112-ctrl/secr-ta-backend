from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import settings
from database import Base, engine, get_db
from models import User, TravelEntry
from schemas import Token, UserCreate, UserOut, TravelCreate, TravelOut
from auth import hash_password, verify_password, create_access_token, get_current_user, require_admin

app = FastAPI(
    title="SECR TA Online Management API",
    version="1.0.0",
    description="Secure API for Admin approved employee TA entries"
)

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    from database import SessionLocal
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.hrms_id == settings.admin_hrms_id).first()
        if not admin:
            admin = User(
                hrms_id=settings.admin_hrms_id,
                password_hash=hash_password(settings.admin_password),
                full_name="System Administrator",
                is_admin=True,
                is_active=True
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "SECR TA Online Management API is running"}

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.hrms_id == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect HRMS ID or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account pending admin approval or inactive")
    token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return Token(access_token=token)

@app.get("/users/me", response_model=UserOut)
def my_profile(current: User = Depends(get_current_user)):
    return current

@app.post("/admin/users", response_model=UserOut)
def admin_create_employee(
    data: UserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    exists = db.query(User).filter(User.hrms_id == data.hrms_id.strip()).first()
    if exists:
        raise HTTPException(status_code=400, detail="HRMS ID already exists")

    user = User(
        hrms_id=data.hrms_id.strip(),
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        department=data.department,
        division=data.division,
        headquarter=data.headquarter,
        pf_no=data.pf_no,
        designation=data.designation,
        pay=data.pay,
        scale_of_pay=data.scale_of_pay,
        bill_unit_no=data.bill_unit_no,
        is_admin=False,
        is_active=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/admin/users", response_model=list[UserOut])
def admin_list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(User).order_by(User.id.desc()).all()

@app.patch("/admin/users/{user_id}/active", response_model=UserOut)
def admin_set_active(user_id: int, active: bool, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.is_admin:
        raise HTTPException(status_code=400, detail="Cannot deactivate admin here")
    user.is_active = active
    db.commit()
    db.refresh(user)
    return user

@app.post("/travels", response_model=TravelOut)
def create_travel(data: TravelCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    amount = round(float(data.rate) * float(data.percentage) / 100, 2)
    entry = TravelEntry(
        user_id=current.id,
        journey_date=data.journey_date,
        transport_mode=data.transport_mode,
        train_no=data.train_no,
        departure_time=data.departure_time,
        arrival_time=data.arrival_time,
        from_station=data.from_station,
        to_station=data.to_station,
        kms=data.kms,
        days=data.days,
        nights=data.nights,
        object_for_journey=data.object_for_journey,
        rate=data.rate,
        percentage=data.percentage,
        amount=amount
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@app.get("/travels/me", response_model=list[TravelOut])
def my_travels(db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    return db.query(TravelEntry).filter(TravelEntry.user_id == current.id).order_by(TravelEntry.id.desc()).all()

@app.put("/travels/{travel_id}", response_model=TravelOut)
def update_travel(travel_id: int, data: TravelCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    entry = db.get(TravelEntry, travel_id)
    if not entry or entry.user_id != current.id:
        raise HTTPException(status_code=404, detail="Travel entry not found")

    for key, value in data.model_dump().items():
        setattr(entry, key, value)
    entry.amount = round(float(data.rate) * float(data.percentage) / 100, 2)
    db.commit()
    db.refresh(entry)
    return entry

@app.delete("/travels/{travel_id}")
def delete_travel(travel_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    entry = db.get(TravelEntry, travel_id)
    if not entry or entry.user_id != current.id:
        raise HTTPException(status_code=404, detail="Travel entry not found")
    db.delete(entry)
    db.commit()
    return {"message": "Travel entry deleted"}

@app.get("/admin/travels", response_model=list[TravelOut])
def admin_all_travels(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    return db.query(TravelEntry).order_by(TravelEntry.id.desc()).all()
