from typing import Optional
from bson import ObjectId
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password
from app.models.user import UserCreate, UserInDB

async def create_user(user_data: UserCreate) -> dict:
    db = get_db()
    existing = await db.users.find_one({"email": user_data.email})
    if existing:
        raise ValueError("Email already registered")
    
    user_doc = {
        "email": user_data.email,
        "full_name": user_data.full_name,
        "tenant_id": user_data.tenant_id,
        "role": user_data.role,
        "hashed_password": get_password_hash(user_data.password),
        "is_active": True,
    }
    result = await db.users.insert_one(user_doc)
    user_doc["id"] = str(result.inserted_id)
    return user_doc

async def authenticate_user(email: str, password: str) -> Optional[dict]:
    db = get_db()
    user = await db.users.find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    user["id"] = str(user["_id"])
    return user

async def get_user_by_id(user_id: str) -> Optional[dict]:
    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user["id"] = str(user["_id"])
    return user

async def get_users_by_tenant(tenant_id: str) -> list:
    db = get_db()
    users = await db.users.find({"tenant_id": tenant_id}).to_list(100)
    for u in users:
        u["id"] = str(u["_id"])
    return users
