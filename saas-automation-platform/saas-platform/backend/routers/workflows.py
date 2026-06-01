from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from typing import List, Optional
from models import Workflow, WorkflowCreate, WorkflowRun, WorkflowStatus
from auth_utils import get_current_user
from database import get_db
from datetime import datetime
from bson import ObjectId
import asyncio, logging

logger = logging.getLogger(__name__)
router = APIRouter()

async def execute_workflow_task(workflow_id: str, run_id: str, tenant_id: str):
    db = get_db()
    logs = []
    try:
        workflow = await db.workflows.find_one({"_id": ObjectId(workflow_id)})
        if not workflow:
            return
        await db.workflow_runs.update_one({"_id": ObjectId(run_id)}, {"$set": {"status": WorkflowStatus.RUNNING}})
        for step in workflow.get("steps", []):
            entry = {"timestamp": datetime.utcnow().isoformat(), "step_id": step["step_id"], "step_name": step["name"], "status": "running"}
            logs.append(entry)
            await asyncio.sleep(0.1)  # simulate async work
            entry["status"] = "completed"
        await db.workflow_runs.update_one(
            {"_id": ObjectId(run_id)},
            {"$set": {"status": WorkflowStatus.COMPLETED, "completed_at": datetime.utcnow(), "logs": logs, "result": {"steps_executed": len(workflow.get("steps", []))}}}
        )
        await db.workflows.update_one(
            {"_id": ObjectId(workflow_id)},
            {"$inc": {"run_count": 1, "success_count": 1}, "$set": {"last_run_at": datetime.utcnow()}}
        )
    except Exception as e:
        logger.error(f"Workflow {workflow_id} failed: {e}")
        await db.workflow_runs.update_one(
            {"_id": ObjectId(run_id)},
            {"$set": {"status": WorkflowStatus.FAILED, "completed_at": datetime.utcnow(), "error": str(e), "logs": logs}}
        )
        await db.workflows.update_one({"_id": ObjectId(workflow_id)}, {"$inc": {"run_count": 1}})

@router.post("/", response_model=Workflow, status_code=201)
async def create_workflow(workflow_data: WorkflowCreate, current_user: dict = Depends(get_current_user)):
    db = get_db()
    doc = {**workflow_data.dict(), "tenant_id": current_user["tenant_id"], "created_by": str(current_user["_id"]),
           "status": WorkflowStatus.PENDING, "run_count": 0, "success_count": 0,
           "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()}
    result = await db.workflows.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return Workflow(**doc)

@router.get("/", response_model=List[Workflow])
async def list_workflows(skip: int = 0, limit: int = 20, current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.workflows.find({"tenant_id": current_user["tenant_id"]}).skip(skip).limit(limit).sort("created_at", -1)
    workflows = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        workflows.append(Workflow(**doc))
    return workflows

@router.post("/{workflow_id}/run", response_model=WorkflowRun)
async def run_workflow(workflow_id: str, background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)):
    db = get_db()
    workflow = await db.workflows.find_one({"_id": ObjectId(workflow_id), "tenant_id": current_user["tenant_id"]})
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    run_doc = {"workflow_id": workflow_id, "tenant_id": current_user["tenant_id"],
               "triggered_by": str(current_user["_id"]), "status": WorkflowStatus.PENDING,
               "started_at": datetime.utcnow(), "logs": []}
    result = await db.workflow_runs.insert_one(run_doc)
    run_doc["id"] = str(result.inserted_id)
    background_tasks.add_task(execute_workflow_task, workflow_id, run_doc["id"], current_user["tenant_id"])
    return WorkflowRun(**run_doc)

@router.get("/{workflow_id}/runs", response_model=List[WorkflowRun])
async def get_workflow_runs(workflow_id: str, limit: int = 10, current_user: dict = Depends(get_current_user)):
    db = get_db()
    cursor = db.workflow_runs.find({"workflow_id": workflow_id}).limit(limit).sort("started_at", -1)
    runs = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        runs.append(WorkflowRun(**doc))
    return runs
