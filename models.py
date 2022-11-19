import uuid
from database import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, String, Integer, Float, Boolean, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)

    name = Column(String,  nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, server_default='user', nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class UserRequest(Base):    
    __tablename__ = 'users_requests'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False, server_default='139837b5-d37a-4d2c-8525-23d7d2af7eac')
    user = relationship('User')
    
    status = Column(Boolean, nullable=False, server_default='False')

    name = Column(String)
    size = Column(Integer)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Flat(Base):
    __tablename__ = 'flats'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)

    request_id = Column(UUID(as_uuid=True), ForeignKey('users_requests.id', ondelete='CASCADE'), nullable=False)
    users_requests = relationship('UserRequest')

    standard = Column(Boolean)
    
    latitude = Column(String)
    longitude = Column(String)
    location = Column(String, nullable=False)
    
    setting = Column(String)
    area = Column(Float, nullable=False)
    object_type = Column(String)
    floor = Column(Integer, nullable=False)
    floors = Column(Integer, nullable=False)

    metro_id = Column(UUID(as_uuid=True), ForeignKey('metros.id'), nullable=False)
    metro = relationship('Metro')

    metro_remoteness = Column(Integer, nullable=False)
    rooms = Column(Integer, nullable=False)
    material = Column(String, nullable=False)
    segment = Column(String, nullable=False)
    kitchen = Column(Float, nullable=False)
    balcony = Column(Boolean, nullable=False)
    renovation = Column(String, nullable=False)
    additions = Column(String)
    price = Column(Float)
    price_per_metre = Column(Float)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Analog(Base):
    __tablename__ = 'analogs'

    id = Column(String, primary_key=True, nullable=False, default=uuid.uuid4)

    source = Column(String)
    offer = Column(String)

    latitude = Column(String)
    longitude = Column(String)
    location = Column(String, nullable=False)
    
    setting = Column(String)
    area = Column(Float, nullable=False)
    object_type = Column(String)
    floor = Column(Integer, nullable=False)
    floors = Column(Integer, nullable=False)

    metro_id = Column(UUID(as_uuid=True), ForeignKey('metros.id'), nullable=False)
    metro = relationship('Metro')

    metro_remoteness = Column(Integer, nullable=False)
    rooms = Column(Integer, nullable=False)
    material = Column(String, nullable=False)
    segment = Column(String, nullable=False)
    kitchen = Column(Float, nullable=False)
    balcony = Column(Boolean, nullable=False)
    renovation = Column(String, nullable=False)
    additions = Column(String)
    price = Column(Float)
    price_per_metre = Column(Float)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Metro(Base):
    __tablename__ = 'metros'

    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)

    name = Column(String,  nullable=False)

    line_id = Column(Integer)

    latitude = Column(String)
    longitude = Column(String)