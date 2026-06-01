from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

class WorkflowStep(BaseModel):
    step_id: str
    name: str
    type: Literal["api_call", "transform", "validate", "notify"]
    config: Dict[str, Any] = {}

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    steps: List[WorkflowStep] = []
    is_active: bool = True

class WorkflowInDB(WorkflowCreate):
    id: str
    tenant_id: str
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    run_count: int = 0
    last_run: Optional[datetime] = None

class WorkflowRun(BaseModel):
    workflow_id: str
    input_data: Dict[str, Any] = {}

class WorkflowRunResult(BaseModel):
    run_id: str
    workflow_id: str
    status: Literal["queued", "running", "completed", "failed"]
    started_at: datetime
    completed_at: Optional[datetime] = None
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
