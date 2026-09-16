from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ScanRequest(BaseModel):
    repo_url: str = Field(..., description="Target GitHub repository clone URL")
    target_branch: str = Field(default="main", description="Target Git branch to audit and enhance")
    jira_issue_id: Optional[str] = Field(default=None, description="Optional Jira Ticket ID")
    coding_standard_repo_url: Optional[str] = Field(
        default=None, 
        description="Optional GitHub repository URL containing department coding standards"
    )


class DimensionScore(BaseModel):
    business_ac: float = Field(default=0.0, description="Business AC Alignment (0-100)")
    resilience: float = Field(default=0.0, description="Technical Edge-Case & Resilience (0-100)")
    coding_standards: float = Field(default=0.0, description="Department Coding Standards Compliance (0-100)")
    assertion_depth: float = Field(default=0.0, description="Assertion Depth & Mocking Quality (0-100)")
    total: float = Field(default=0.0, description="Weighted composite score (0-100)")


class BlindspotItem(BaseModel):
    id: str
    category: str  # business_ac, resilience, coding_standard, assertion
    title: str
    description: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    status: str    # OPEN, RESOLVED
    target_file: Optional[str] = None


class ScanReport(BaseModel):
    scan_id: str
    repo_url: str
    target_branch: str
    enhanced_branch: str
    status: str  # PENDING, RUNNING, COMPLETED, FAILED
    original_score: DimensionScore
    enhanced_score: Optional[DimensionScore] = None
    blindspots: List[BlindspotItem] = Field(default_factory=list)
    resolved_blindspot_ids: List[str] = Field(default_factory=list)
    generated_test_files: List[str] = Field(default_factory=list)
    pr_url: Optional[str] = None
    execution_time_seconds: float = 0.0


class AgentThought(BaseModel):
    timestamp: str
    stage: str
    message: str
    level: str = "INFO"
    metadata: Dict[str, Any] = Field(default_factory=dict)
