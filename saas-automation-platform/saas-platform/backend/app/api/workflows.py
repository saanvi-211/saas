from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from app.core.deps import get_current_user
from app.models.workflow import WorkflowCreate, WorkflowRun
from app.services.workflow_service import create_workflow, get_workflows, execute_workflow

router = APIRouter()

@router.post("/", status_code=201)
async def create(workflow_data: WorkflowCreate, current_user: dict = Depends(get_current_user)):
    return await create_workflow(workflow_data, current_user["tenant_id"], current_user["sub"])

@router.get("/")
async def list_workflows(current_user: dict = Depends(get_current_user)):
    return await get_workflows(current_user["tenant_id"])

@router.post("/{workflow_id}/run")
async def run_workflow(
    workflow_id: str,
    run_data: WorkflowRun,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    background_tasks.add_task(execute_workflow, workflow_id, run_data.input_data, current_user["tenant_id"])
    return {"message": "Workflow execution queued", "workflow_id": workflow_id}
