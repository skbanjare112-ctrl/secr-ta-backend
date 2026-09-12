from datetime import datetime
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    hrms_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(200), default="")
    department: Mapped[str] = mapped_column(String(150), default="")
    division: Mapped[str] = mapped_column(String(150), default="")
    headquarter: Mapped[str] = mapped_column(String(150), default="")
    pf_no: Mapped[str] = mapped_column(String(100), default="")
    designation: Mapped[str] = mapped_column(String(150), default="")
    pay: Mapped[float] = mapped_column(Float, default=0)
    scale_of_pay: Mapped[str] = mapped_column(String(100), default="")
    bill_unit_no: Mapped[str] = mapped_column(String(100), default="")
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    travels = relationship("TravelEntry", back_populates="user", cascade="all, delete-orphan")

class TravelEntry(Base):
    __tablename__ = "travel_entries"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    journey_date: Mapped[str] = mapped_column(String(20))
    transport_mode: Mapped[str] = mapped_column(String(100), default="")
    train_no: Mapped[str] = mapped_column(String(100), default="")
    departure_time: Mapped[str] = mapped_column(String(20), default="")
    arrival_time: Mapped[str] = mapped_column(String(20), default="")
    from_station: Mapped[str] = mapped_column(String(200), default="")
    to_station: Mapped[str] = mapped_column(String(200), default="")
    kms: Mapped[float] = mapped_column(Float, default=0)
    days: Mapped[float] = mapped_column(Float, default=0)
    nights: Mapped[float] = mapped_column(Float, default=0)
    object_for_journey: Mapped[str] = mapped_column(Text, default="")
    rate: Mapped[float] = mapped_column(Float, default=625)
    percentage: Mapped[float] = mapped_column(Float, default=100)
    amount: Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="travels")
