from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class LicenseCategory(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    BE = "BE"
    CE = "CE"
    DE = "DE"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    full_name = Column(String)
    phone_number = Column(String)
    license_number = Column(String)
    license_category = Column(Enum(LicenseCategory))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    rentals = relationship("Rental", back_populates="user")

class Car(Base):
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True)
    model = Column(String)
    year = Column(Integer)
    license_plate = Column(String, unique=True)
    daily_rate = Column(Float)
    is_available = Column(Boolean, default=True)
    required_license = Column(Enum(LicenseCategory))
    
    rentals = relationship("Rental", back_populates="car")

class Rental(Base):
    __tablename__ = "rentals"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    car_id = Column(Integer, ForeignKey("cars.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    total_cost = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="rentals")
    car = relationship("Car", back_populates="rentals")