from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.core.database import get_db
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_analytics(current_user: dict = Depends(get_current_user)):
    db = get_db()
    tenant_id = current_user["tenant_id"]
    
    total_workflows = await db.workflows.count_documents({"tenant_id": tenant_id})
    total_runs = await db.workflow_runs.count_documents({"tenant_id": tenant_id})
    completed_runs = await db.workflow_runs.count_documents({"tenant_id": tenant_id, "status": "completed"})
    
    # Aggregation pipeline for runs per day (last 7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    pipeline = [
        {"$match": {"tenant_id": tenant_id, "started_at": {"$gte": seven_days_ago}}},
        {"$group": {
            "_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$started_at"}},
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id": 1}}
    ]
    daily_runs = await db.workflow_runs.aggregate(pipeline).to_list(7)
    
    return {
        "total_workflows": total_workflows,
        "total_runs": total_runs,
        "success_rate": round(completed_runs / total_runs * 100, 1) if total_runs > 0 else 0,
        "daily_runs": daily_runs,
    }
