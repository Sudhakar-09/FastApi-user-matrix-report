from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session # type: ignore
from database import get_db ,engine
from crud import create_user, get_user_by_id, update_user, delete_user, create_site_role, delete_site_role, create_user_org, delete_user_org, get_active_users_report
from schemas import UserCreate, UserUpdate, StatusResponse, UserReportResponse, UserResponse
import models
from fastapi.responses import JSONResponse

app = FastAPI()

# Automatically create tables in the database
models.Base.metadata.create_all(bind=engine)


# Report endpoint
@app.get("/users/report", status_code=status.HTTP_200_OK)
def get_active_user_report(db: Session = Depends(get_db)):
    response_data = get_active_users_report(db)
    return JSONResponse(content=response_data)


# User CRUD operations
@app.post("/users/", response_model=StatusResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=StatusResponse, status_code=status.HTTP_200_OK)
def update_existing_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return update_user(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=StatusResponse, status_code=status.HTTP_200_OK)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db=db, user_id=user_id)

# UserSiteRole CRUD operations
@app.post("/user_site_roles/", response_model=StatusResponse, status_code=status.HTTP_201_CREATED)
def create_new_site_role(user_id: int, site_role: str, db: Session = Depends(get_db)):
    return create_site_role(db=db, user_id=user_id, site_role=site_role)

@app.delete("/user_site_roles/{site_role_id}", response_model=StatusResponse, status_code=status.HTTP_200_OK)
def delete_existing_site_role(site_role_id: int, db: Session = Depends(get_db)):
    return delete_site_role(db=db, site_role_id=site_role_id)

# UserOrg CRUD operations
@app.post("/user_orgs/", response_model=StatusResponse, status_code=status.HTTP_201_CREATED)
def create_new_user_org(user_id: int, org_name: str, org_role: str, db: Session = Depends(get_db)):
    return create_user_org(db=db, user_id=user_id, org_name=org_name, org_role=org_role)


@app.delete("/user_orgs/{org_id}", response_model=StatusResponse, status_code=status.HTTP_200_OK)
def delete_existing_user_org(org_id: int, db: Session = Depends(get_db)):
    return delete_user_org(db=db, org_id=org_id)

