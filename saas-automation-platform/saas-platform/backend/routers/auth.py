from fastapi import APIRouter, HTTPException, status
from models import UserCreate, UserLogin, Token, User
from auth_utils import get_password_hash, verify_password, create_access_token, create_refresh_token
from database import get_db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=User, status_code=201)
async def register(user_data: UserCreate):
    db = get_db()
    if await db.users.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    doc = {
        "email": user_data.email, "full_name": user_data.full_name,
        "tenant_id": user_data.tenant_id, "role": user_data.role,
        "hashed_password": get_password_hash(user_data.password),
        "is_active": True, "created_at": datetime.utcnow(),
    }
    result = await db.users.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return User(**doc)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    db = get_db()
    user = await db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.get("is_active"):
        raise HTTPException(status_code=403, detail="Account disabled")
    data = {"sub": str(user["_id"]), "email": user["email"], "tenant_id": user["tenant_id"], "role": user["role"]}
    return Token(access_token=create_access_token(data), refresh_token=create_refresh_token(data))
