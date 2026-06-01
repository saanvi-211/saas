from fastapi import APIRouter, Depends
from auth_utils import get_current_user
from database import get_db
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/summary")
async def get_analytics_summary(current_user: dict = Depends(get_current_user)):
    db = get_db()
    tid = current_user["tenant_id"]
    total_workflows = await db.workflows.count_documents({"tenant_id": tid})
    total_runs = await db.workflow_runs.count_documents({"tenant_id": tid})
    successful_runs = await db.workflow_runs.count_documents({"tenant_id": tid, "status": "completed"})
    last_7d = datetime.utcnow() - timedelta(days=7)
    recent_runs = await db.workflow_runs.count_documents({"tenant_id": tid, "started_at": {"$gte": last_7d}})
    success_rate = (successful_runs / total_runs * 100) if total_runs > 0 else 0
    return {"total_workflows": total_workflows, "total_runs": total_runs,
            "successful_runs": successful_runs, "success_rate": round(success_rate, 2), "recent_runs_7d": recent_runs}

@router.get("/workflow-activity")
async def get_workflow_activity(days: int = 30, current_user: dict = Depends(get_current_user)):
    db = get_db()
    start_date = datetime.utcnow() - timedelta(days=days)
    pipeline = [
        {"$match": {"tenant_id": current_user["tenant_id"], "started_at": {"$gte": start_date}}},
        {"$group": {"_id": {"year": {"$year": "$started_at"}, "month": {"$month": "$started_at"}, "day": {"$dayOfMonth": "$started_at"}},
                    "total": {"$sum": 1},
                    "completed": {"$sum": {"$cond": [{"$eq": ["$status", "completed"]}, 1, 0]}},
                    "failed": {"$sum": {"$cond": [{"$eq": ["$status", "failed"]}, 1, 0]}}}},
        {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1}}
    ]
    result = []
    async for doc in db.workflow_runs.aggregate(pipeline):
        result.append({"date": f"{doc['_id']['year']}-{doc['_id']['month']:02d}-{doc['_id']['day']:02d}",
                        "total": doc["total"], "completed": doc["completed"], "failed": doc["failed"]})
    return result
