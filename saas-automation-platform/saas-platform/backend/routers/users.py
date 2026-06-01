from fastapi import APIRouter, Depends, HTTPException
from models import User, UserRole
from auth_utils import get_current_user
from database import get_db

router = APIRouter()

@router.get("/me", response_model=User)
async def get_me(current_user: dict = Depends(get_current_user)):
    current_user["id"] = str(current_user.pop("_id"))
    return User(**current_user)

@router.get("/")
async def list_users(current_user: dict = Depends(get_current_user)):
    if current_user["role"] not in (UserRole.ADMIN, UserRole.MANAGER):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    db = get_db()
    users = []
    async for doc in db.users.find({"tenant_id": current_user["tenant_id"]}, {"hashed_password": 0}):
        doc["id"] = str(doc.pop("_id"))
        users.append(doc)
    return users
