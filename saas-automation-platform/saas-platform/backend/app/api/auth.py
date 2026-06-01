from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, LoginRequest, TokenResponse, UserResponse
from app.services.user_service import create_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate):
    try:
        user = await create_user(user_data)
        return UserResponse(**user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    user = await authenticate_user(credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    token = create_access_token({"sub": user["id"], "role": user["role"], "tenant_id": user["tenant_id"]})
    return TokenResponse(access_token=token, user=UserResponse(**user))
