from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import User, UserSiteRole, UserOrg
from schemas import UserCreate, UserUpdate, StatusResponse
from sqlalchemy import func


# CRUD for Users
def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        address=user.address,
        role=user.role
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            "status": "success",
            "message": "User created successfully"
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "status": "error",
            "message": f"Error creating user: {str(e)}"
        }

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user.is_active is not None:
            db_user.is_active = user.is_active
        db_user.updated_at = func.now()
        db.commit()
        db.refresh(db_user)
        return {
            "status": "success",
            "message": "User updated successfully"
        }
    return {
        "status": "error",
        "message": "User not found"
    }

def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return {
            "status": "success",
            "message": "User deleted successfully"
        }
    return {
        "status": "error",
        "message": "User not found"
    }


# CRUD for UserSiteRole
def create_site_role(db: Session, user_id: int, site_role: str):
    db_site_role = UserSiteRole(user_id=user_id, site_role=site_role)
    try:
        db.add(db_site_role)
        db.commit()
        db.refresh(db_site_role)
        return {
            "status": "success",
            "message": "Site role added successfully"
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "status": "error",
            "message": f"Error adding site role: {str(e)}"
        }

def delete_site_role(db: Session, site_role_id: int):
    db_site_role = db.query(UserSiteRole).filter(UserSiteRole.id == site_role_id).first()
    if db_site_role:
        db.delete(db_site_role)
        db.commit()
        return {
            "status": "success",
            "message": "Site role deleted successfully"
        }
    return {
        "status": "error",
        "message": "Site role not found"
    }


def create_user_org(db: Session, user_id: int, org_name: str, org_role: Optional[str] = None):
    
    db_org = UserOrg(user_id=user_id, org_name=org_name, org_role=org_role)
    try:
        db.add(db_org)
        db.commit()
        db.refresh(db_org)
        return {
            "status": "success",
            "message": "User organization added successfully",
            "data": {
                "id": db_org.id,
                "user_id": db_org.user_id,
                "org_name": db_org.org_name,
                "org_role": db_org.org_role
            }
        }
    except SQLAlchemyError as e:
        db.rollback()
        return {
            "status": "error",
            "message": f"Error adding user organization: {str(e)}"
        }

def delete_user_org(db: Session, org_id: int):
    db_org = db.query(UserOrg).filter(UserOrg.id == org_id).first()
    if db_org:
        db.delete(db_org)
        db.commit()
        return {
            "status": "success",
            "message": "User organization deleted successfully"
        }
    return {
        "status": "error",
        "message": "User organization not found"
    }



# Active Users Report
def get_active_users_report(db: Session):
    try:
        # Query to fetch active users with their associated site roles and organizations
        result = db.query(User, UserSiteRole, UserOrg) \
            .join(UserSiteRole, User.id == UserSiteRole.user_id, isouter=True) \
            .join(UserOrg, User.id == UserOrg.user_id, isouter=True) \
            .filter(User.is_active == True) \
            .all()

        # Check if no active users found
        if not result:
            return {
                "status": "error",
                "message": "No active users found"
            }

        # Function to format datetime
        def format_datetime(dt):
            return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None

        # Construct the report for active users
        users_report = []
        for user, site_role, org in result:
            users_report.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "site_role": site_role.site_role if site_role else None,  # Single role value
                "organization": org.org_name if org else None,  # Single organization value
                "created_at": format_datetime(user.created_at),  # Format created_at
                "updated_at": format_datetime(user.updated_at),  # Format updated_at
                "is_active": user.is_active
            })

        return {
            "status": "success",
            "message": "Report fetched successfully",
            "data": users_report
        }

    except SQLAlchemyError as e:
        # Log the detailed error and return a generic message
        return {
            "status": "error",
            "message": f"Error fetching report: {str(e)}"
        }
    except Exception as e:
        # Catch any other exceptions to avoid unhandled errors
        return {
            "status": "error",
            "message": f"Unexpected error: {str(e)}"
        }