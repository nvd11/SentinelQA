from typing import Dict, Any, Optional
from ..agent.orchestrator import AgentOrchestrator
from ..models.schemas import ScanRequest


class ScanService:
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self._reports: Dict[str, Any] = {}

    def get_orchestrator(self) -> AgentOrchestrator:
        return self.orchestrator

    def store_report(self, scan_id: str, report: Dict[str, Any]) -> None:
        self._reports[scan_id] = report

    def get_report(self, scan_id: str) -> Optional[Dict[str, Any]]:
        return self._reports.get(scan_id)


scan_service = ScanService()
