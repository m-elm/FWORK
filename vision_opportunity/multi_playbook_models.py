"""
Multi-playbook data models for interconnected startup playbook agents.
Extends the existing models to support cross-playbook dependencies and shared state.
"""

from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from models import WorkflowState, UserResponse, Citation, CostMetrics

class PlaybookType(str, Enum):
    VISION_OPPORTUNITY = "vision_opportunity"
    CUSTOMER_DISCOVERY = "customer_discovery" 
    BUSINESS_MODEL = "business_model"
    PRODUCT_STRATEGY = "product_strategy"
    UX_DESIGN = "ux_design"
    TECHNICAL_DEVELOPMENT = "technical_development"
    TEAM_CULTURE = "team_culture"
    FINANCIAL_PLANNING = "financial_planning"
    PROJECT_EXECUTION = "project_execution"
    LAUNCH_GROWTH = "launch_growth"
    DATA_ANALYTICS = "data_analytics"
    BRAND_COMMUNICATION = "brand_communication"
    LEGAL_COMPLIANCE = "legal_compliance"
    PARTNERSHIPS = "partnerships"
    CONTINUOUS_IMPROVEMENT = "continuous_improvement"

class PlaybookPriority(str, Enum):
    HIGH = "high"          # Core foundation playbooks
    MEDIUM_HIGH = "medium_high"  # Important for execution
    MEDIUM = "medium"      # Supporting playbooks
    MEDIUM_LOW = "medium_low"    # Enhancement playbooks

class DependencyType(str, Enum):
    REQUIRES = "requires"          # Hard dependency
    INFLUENCES = "influences"      # Soft dependency
    UPDATES = "updates"           # One-way update trigger
    SYNCS = "syncs"              # Bi-directional sync

class PlaybookDependency(BaseModel):
    from_playbook: PlaybookType
    to_playbook: PlaybookType
    dependency_type: DependencyType
    description: str
    trigger_fields: List[str] = Field(description="Fields that trigger this dependency")
    update_targets: List[str] = Field(description="Fields that get updated in target playbook")
    priority: int = Field(ge=1, le=10, description="Priority of this dependency")

class PlaybookStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress" 
    SUFFICIENT = "sufficient"
    COMPLETE = "complete"
    NEEDS_UPDATE = "needs_update"

class SharedKnowledge(BaseModel):
    """Central repository of shared information across playbooks"""
    company_info: Dict[str, Any] = Field(default_factory=dict)
    target_market: Dict[str, Any] = Field(default_factory=dict)
    product_details: Dict[str, Any] = Field(default_factory=dict)
    financial_data: Dict[str, Any] = Field(default_factory=dict)
    team_info: Dict[str, Any] = Field(default_factory=dict)
    timeline: Dict[str, Any] = Field(default_factory=dict)
    last_updated: datetime = Field(default_factory=datetime.now)
    update_history: List[Dict[str, Any]] = Field(default_factory=list)

class PlaybookState(BaseModel):
    """State for individual playbook"""
    playbook_type: PlaybookType
    status: PlaybookStatus = PlaybookStatus.NOT_STARTED
    priority: PlaybookPriority
    progress: float = Field(ge=0.0, le=1.0, default=0.0)
    workflow_state: WorkflowState
    generated_artifacts: Dict[str, Any] = Field(default_factory=dict)
    dependencies_met: bool = False
    blocked_by: List[PlaybookType] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.now)
    
class CrossPlaybookUpdate(BaseModel):
    """Represents an update that affects multiple playbooks"""
    source_playbook: PlaybookType
    affected_playbooks: List[PlaybookType]
    update_type: str
    changes: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.now)
    propagated: bool = False

class MultiPlaybookWorkflowState(BaseModel):
    """Overall state managing all playbooks"""
    playbooks: Dict[PlaybookType, PlaybookState] = Field(default_factory=dict)
    shared_knowledge: SharedKnowledge = Field(default_factory=SharedKnowledge)
    dependencies: List[PlaybookDependency] = Field(default_factory=list)
    active_playbook: Optional[PlaybookType] = None
    pending_updates: List[CrossPlaybookUpdate] = Field(default_factory=list)
    overall_progress: float = Field(ge=0.0, le=1.0, default=0.0)
    cost_metrics: CostMetrics = Field(default_factory=lambda: CostMetrics(
        tokens_used=0, computation_time=0.0, api_calls=0
    ))
    
    def get_available_playbooks(self) -> List[PlaybookType]:
        """Get playbooks that can be started (dependencies met)"""
        available = []
        for playbook_type, state in self.playbooks.items():
            if state.status == PlaybookStatus.NOT_STARTED and state.dependencies_met:
                available.append(playbook_type)
            elif state.status in [PlaybookStatus.IN_PROGRESS, PlaybookStatus.SUFFICIENT]:
                available.append(playbook_type)
        return available
    
    def update_shared_knowledge(self, key: str, value: Any, source_playbook: PlaybookType):
        """Update shared knowledge and track the change"""
        # Update the knowledge
        keys = key.split('.')
        target = self.shared_knowledge
        for k in keys[:-1]:
            if k not in target.__dict__:
                setattr(target, k, {})
            target = getattr(target, k)
        
        old_value = target.get(keys[-1]) if hasattr(target, 'get') else getattr(target, keys[-1], None)
        
        if hasattr(target, 'get'):
            target[keys[-1]] = value
        else:
            setattr(target, keys[-1], value)
            
        # Track the update
        self.shared_knowledge.update_history.append({
            'key': key,
            'old_value': old_value,
            'new_value': value,
            'source_playbook': source_playbook.value,
            'timestamp': datetime.now()
        })
        
        self.shared_knowledge.last_updated = datetime.now()
        
        # Create cross-playbook update
        affected = self._find_affected_playbooks(key, source_playbook)
        if affected:
            update = CrossPlaybookUpdate(
                source_playbook=source_playbook,
                affected_playbooks=affected,
                update_type="knowledge_update",
                changes={key: value}
            )
            self.pending_updates.append(update)
    
    def _find_affected_playbooks(self, key: str, source_playbook: PlaybookType) -> List[PlaybookType]:
        """Find playbooks affected by a knowledge update"""
        affected = []
        for dependency in self.dependencies:
            if (dependency.from_playbook == source_playbook and 
                any(field in key for field in dependency.trigger_fields)):
                affected.append(dependency.to_playbook)
        return affected

class AgentCoordinationMessage(BaseModel):
    """Message format for agent coordination"""
    from_agent: str
    to_agent: str
    message_type: str  # "update", "request", "response", "notification"
    content: Dict[str, Any]
    priority: int = Field(ge=1, le=10, default=5)
    timestamp: datetime = Field(default_factory=datetime.now)
    requires_response: bool = False
    response_timeout: Optional[int] = Field(default=None, description="Timeout in seconds") 