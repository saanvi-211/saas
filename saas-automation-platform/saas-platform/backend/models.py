from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    VIEWER = "viewer"

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    full_name: str
    tenant_id: str
    role: UserRole = UserRole.VIEWER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    tenant_id: str
    role: UserRole = UserRole.VIEWER

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class WorkflowStep(BaseModel):
    step_id: str
    name: str
    action: str
    config: Dict[str, Any] = {}
    retry_count: int = 0
    timeout_seconds: int = 30

class Workflow(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    tenant_id: str
    created_by: str
    steps: List[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.PENDING
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_run_at: Optional[datetime] = None
    run_count: int = 0
    success_count: int = 0

class WorkflowCreate(BaseModel):
    name: str
    description: str
    steps: List[WorkflowStep]
    tags: List[str] = []

class WorkflowRun(BaseModel):
    id: Optional[str] = None
    workflow_id: str
    tenant_id: str
    triggered_by: str
    status: WorkflowStatus = WorkflowStatus.PENDING
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    logs: List[Dict[str, Any]] = []
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
