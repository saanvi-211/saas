from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import get_current_user, require_admin
from app.services.user_service import get_users_by_tenant, get_user_by_id

router = APIRouter()

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    user = await get_user_by_id(current_user["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.pop("hashed_password", None)
    return user

@router.get("/")
async def list_users(current_user: dict = Depends(require_admin)):
    users = await get_users_by_tenant(current_user["tenant_id"])
    for u in users:
        u.pop("hashed_password", None)
    return users
