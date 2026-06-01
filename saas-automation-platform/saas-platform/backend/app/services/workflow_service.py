import asyncio
import uuid
from datetime import datetime
from typing import Optional
from bson import ObjectId
from app.core.database import get_db
from app.models.workflow import WorkflowCreate

async def create_workflow(workflow_data: WorkflowCreate, tenant_id: str, user_id: str) -> dict:
    db = get_db()
    doc = {
        **workflow_data.dict(),
        "tenant_id": tenant_id,
        "created_by": user_id,
        "run_count": 0,
        "last_run": None,
        "created_at": datetime.utcnow(),
    }
    result = await db.workflows.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc

async def get_workflows(tenant_id: str) -> list:
    db = get_db()
    workflows = await db.workflows.find({"tenant_id": tenant_id}).to_list(100)
    for w in workflows:
        w["id"] = str(w["_id"])
    return workflows

async def execute_workflow(workflow_id: str, input_data: dict, tenant_id: str) -> dict:
    """Background task: simulates async step execution."""
    db = get_db()
    run_id = str(uuid.uuid4())
    run_doc = {
        "run_id": run_id,
        "workflow_id": workflow_id,
        "tenant_id": tenant_id,
        "status": "running",
        "started_at": datetime.utcnow(),
        "input": input_data,
    }
    await db.workflow_runs.insert_one(run_doc)
    
    # Simulate async processing
    await asyncio.sleep(0.1)
    
    await db.workflow_runs.update_one(
        {"run_id": run_id},
        {"$set": {"status": "completed", "completed_at": datetime.utcnow(), "output": {"processed": True, "items": len(input_data)}}}
    )
    await db.workflows.update_one(
        {"_id": ObjectId(workflow_id)},
        {"$inc": {"run_count": 1}, "$set": {"last_run": datetime.utcnow()}}
    )
    return {"run_id": run_id, "status": "completed"}
