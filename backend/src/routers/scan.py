import json
from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from ..models.schemas import ScanRequest
from ..services.scan_service import scan_service
from ..utils.logger import logger

router = APIRouter(prefix="/api/v1", tags=["Scan & Stream"])


@router.post("/scan")
async def trigger_scan(request: ScanRequest):
    """Initiates an autonomous SentinelQA scan, returning a Server-Sent Events stream."""
    logger.info(f"Incoming scan request: repo={request.repo_url}, branch={request.target_branch}")

    async def event_generator():
        orchestrator = scan_service.get_orchestrator()
        async for event in orchestrator.execute_scan_workflow(request):
            if event["type"] == "result":
                scan_service.store_report(event["data"]["scan_id"], event["data"])
            yield {
                "event": event["type"],
                "data": json.dumps(event["data"])
            }

    return EventSourceResponse(event_generator())


@router.get("/report/{scan_id}")
async def get_report(scan_id: str):
    """Retrieves an existing scan report by its scan ID."""
    report = scan_service.get_report(scan_id)
    if not report:
        raise HTTPException(status_code=404, detail="Scan report not found")
    return report
