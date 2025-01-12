from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from sqlalchemy.sql import func # type: ignore
from sqlalchemy.ext.declarative import declarative_base

# Base class for the models
Base = declarative_base()


# User Model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True)  # Added length specification
    email = Column(String(255), unique=True, index=True)  # Added length specification
    first_name = Column(String(255))  # Added length specification
    last_name = Column(String(255))  # Added length specification
    password = Column(String(255))  # Added length specification
    phone_number = Column(String(20), nullable=True)  # Store phone number as a string
    address = Column(String(200), nullable=True)  # Add address here
    role = Column(String(20))

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    site_roles = relationship("UserSiteRole", back_populates="user", cascade="all, delete-orphan")
    org_roles = relationship("UserOrg", back_populates="user", cascade="all, delete-orphan")

# UserSiteRole Model
class UserSiteRole(Base):
    __tablename__ = "user_site_roles"
    
    id = Column(Integer, primary_key=True, index=True)
    site_role = Column(String(255))  # Added length specification
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="site_roles")

# UserOrg Model
class UserOrg(Base):
    __tablename__ = "user_orgs"
    
    id = Column(Integer, primary_key=True, index=True)
    org_name = Column(String(255))  # Added length specification
    org_role = Column(String(255))  # Added length specification
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="org_roles")
