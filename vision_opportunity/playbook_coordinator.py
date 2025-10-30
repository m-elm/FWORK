"""
Central coordinator for managing multiple interconnected startup playbooks.
This is the brain that orchestrates all playbook agents and manages dependencies.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pathlib import Path

from multi_playbook_models import (
    PlaybookType, PlaybookPriority, PlaybookStatus, DependencyType,
    PlaybookDependency, PlaybookState, MultiPlaybookWorkflowState,
    SharedKnowledge, CrossPlaybookUpdate, AgentCoordinationMessage
)
from models import WorkflowState, CostMetrics
from agents import BaseAgent


class PlaybookCoordinator(BaseAgent):
    """Central coordinator managing all playbook agents and their interactions."""
    
    def __init__(self, use_ai: bool = True):
        super().__init__("PlaybookCoordinator", {
            "max_tokens": 10000, 
            "max_api_calls": 100
        })
        self.use_ai = use_ai
        self.state = MultiPlaybookWorkflowState()
        self.playbook_agents: Dict[PlaybookType, Any] = {}
        self.message_queue: List[AgentCoordinationMessage] = []
        self.dependencies = self._initialize_dependencies()
        self._initialize_playbooks()
        
    def _initialize_dependencies(self) -> List[PlaybookDependency]:
        """Define the dependencies between playbooks based on the framework."""
        return [
            # Vision & Opportunity influences most other playbooks
            PlaybookDependency(
                from_playbook=PlaybookType.VISION_OPPORTUNITY,
                to_playbook=PlaybookType.CUSTOMER_DISCOVERY,
                dependency_type=DependencyType.INFLUENCES,
                description="Vision statement guides customer discovery questions",
                trigger_fields=["target_market", "problem_statement", "vision"],
                update_targets=["customer_segments", "interview_scripts"],
                priority=9
            ),
            PlaybookDependency(
                from_playbook=PlaybookType.VISION_OPPORTUNITY,
                to_playbook=PlaybookType.BUSINESS_MODEL,
                dependency_type=DependencyType.INFLUENCES,
                description="TAM and market analysis inform business model",
                trigger_fields=["tam_calculation", "market_size", "target_market"],
                update_targets=["revenue_model", "pricing_strategy"],
                priority=8
            ),
            
            # Customer Discovery influences Product Strategy and Business Model
            PlaybookDependency(
                from_playbook=PlaybookType.CUSTOMER_DISCOVERY,
                to_playbook=PlaybookType.PRODUCT_STRATEGY,
                dependency_type=DependencyType.REQUIRES,
                description="Customer insights are required for product strategy",
                trigger_fields=["customer_personas", "pain_points", "jtbd"],
                update_targets=["value_proposition", "product_roadmap", "feature_prioritization"],
                priority=10
            ),
            PlaybookDependency(
                from_playbook=PlaybookType.CUSTOMER_DISCOVERY,
                to_playbook=PlaybookType.BUSINESS_MODEL,
                dependency_type=DependencyType.UPDATES,
                description="Customer validation updates business model assumptions",
                trigger_fields=["willingness_to_pay", "customer_segments"],
                update_targets=["pricing_strategy", "customer_acquisition_cost"],
                priority=7
            ),
            
            # Product Strategy influences UX Design and Technical Development
            PlaybookDependency(
                from_playbook=PlaybookType.PRODUCT_STRATEGY,
                to_playbook=PlaybookType.UX_DESIGN,
                dependency_type=DependencyType.REQUIRES,
                description="Product strategy defines UX requirements",
                trigger_fields=["user_stories", "feature_prioritization", "value_proposition"],
                update_targets=["user_journey_maps", "wireframes", "design_system"],
                priority=9
            ),
            PlaybookDependency(
                from_playbook=PlaybookType.PRODUCT_STRATEGY,
                to_playbook=PlaybookType.TECHNICAL_DEVELOPMENT,
                dependency_type=DependencyType.REQUIRES,
                description="Product roadmap drives technical architecture",
                trigger_fields=["product_roadmap", "technical_requirements"],
                update_targets=["system_architecture", "technology_stack"],
                priority=8
            ),
            
            # Business Model influences Financial Planning
            PlaybookDependency(
                from_playbook=PlaybookType.BUSINESS_MODEL,
                to_playbook=PlaybookType.FINANCIAL_PLANNING,
                dependency_type=DependencyType.REQUIRES,
                description="Business model defines financial projections",
                trigger_fields=["revenue_model", "unit_economics", "pricing_strategy"],
                update_targets=["financial_projections", "funding_requirements"],
                priority=9
            ),
            
            # UX Design and Technical Development influence Project Execution
            PlaybookDependency(
                from_playbook=PlaybookType.UX_DESIGN,
                to_playbook=PlaybookType.PROJECT_EXECUTION,
                dependency_type=DependencyType.INFLUENCES,
                description="UX design affects development timeline",
                trigger_fields=["design_complexity", "prototype_completion"],
                update_targets=["sprint_planning", "resource_allocation"],
                priority=6
            ),
            PlaybookDependency(
                from_playbook=PlaybookType.TECHNICAL_DEVELOPMENT,
                to_playbook=PlaybookType.PROJECT_EXECUTION,
                dependency_type=DependencyType.INFLUENCES,
                description="Technical architecture affects project planning",
                trigger_fields=["architecture_complexity", "technology_decisions"],
                update_targets=["development_methodology", "timeline"],
                priority=7
            ),
            
            # Financial Planning influences Team & Culture
            PlaybookDependency(
                from_playbook=PlaybookType.FINANCIAL_PLANNING,
                to_playbook=PlaybookType.TEAM_CULTURE,
                dependency_type=DependencyType.INFLUENCES,
                description="Budget constraints affect hiring and culture",
                trigger_fields=["funding_status", "burn_rate", "team_budget"],
                update_targets=["hiring_plan", "compensation_structure"],
                priority=6
            ),
            
            # Multiple playbooks influence Launch & Growth
            PlaybookDependency(
                from_playbook=PlaybookType.PRODUCT_STRATEGY,
                to_playbook=PlaybookType.LAUNCH_GROWTH,
                dependency_type=DependencyType.REQUIRES,
                description="Product strategy defines go-to-market approach",
                trigger_fields=["target_segments", "value_proposition"],
                update_targets=["gtm_strategy", "channel_strategy"],
                priority=8
            ),
            PlaybookDependency(
                from_playbook=PlaybookType.BUSINESS_MODEL,
                to_playbook=PlaybookType.LAUNCH_GROWTH,
                dependency_type=DependencyType.REQUIRES,
                description="Business model defines growth metrics",
                trigger_fields=["unit_economics", "revenue_model"],
                update_targets=["growth_metrics", "acquisition_strategy"],
                priority=7
            ),
        ]
    
    def _initialize_playbooks(self):
        """Initialize all playbook states with their priorities."""
        playbook_priorities = {
            PlaybookType.VISION_OPPORTUNITY: PlaybookPriority.HIGH,
            PlaybookType.CUSTOMER_DISCOVERY: PlaybookPriority.HIGH,
            PlaybookType.BUSINESS_MODEL: PlaybookPriority.HIGH,
            PlaybookType.PRODUCT_STRATEGY: PlaybookPriority.HIGH,
            PlaybookType.UX_DESIGN: PlaybookPriority.HIGH,
            PlaybookType.TECHNICAL_DEVELOPMENT: PlaybookPriority.MEDIUM_HIGH,
            PlaybookType.TEAM_CULTURE: PlaybookPriority.MEDIUM_HIGH,
            PlaybookType.FINANCIAL_PLANNING: PlaybookPriority.MEDIUM,
            PlaybookType.PROJECT_EXECUTION: PlaybookPriority.MEDIUM,
            PlaybookType.LAUNCH_GROWTH: PlaybookPriority.MEDIUM,
            PlaybookType.DATA_ANALYTICS: PlaybookPriority.MEDIUM,
            PlaybookType.BRAND_COMMUNICATION: PlaybookPriority.MEDIUM_LOW,
            PlaybookType.LEGAL_COMPLIANCE: PlaybookPriority.MEDIUM_LOW,
            PlaybookType.PARTNERSHIPS: PlaybookPriority.MEDIUM_LOW,
            PlaybookType.CONTINUOUS_IMPROVEMENT: PlaybookPriority.MEDIUM_LOW,
        }
        
        for playbook_type, priority in playbook_priorities.items():
            self.state.playbooks[playbook_type] = PlaybookState(
                playbook_type=playbook_type,
                priority=priority,
                workflow_state=WorkflowState(),
                dependencies_met=self._check_dependencies_met(playbook_type)
            )
        
        # Set initial dependencies
        self.state.dependencies = self.dependencies
        
        # Vision & Opportunity can start immediately
        self.state.playbooks[PlaybookType.VISION_OPPORTUNITY].dependencies_met = True
    
    def _check_dependencies_met(self, playbook_type: PlaybookType) -> bool:
        """Check if a playbook's dependencies are satisfied."""
        required_deps = [
            dep for dep in self.dependencies 
            if dep.to_playbook == playbook_type and dep.dependency_type == DependencyType.REQUIRES
        ]
        
        for dep in required_deps:
            source_state = self.state.playbooks.get(dep.from_playbook)
            if not source_state or source_state.status not in [PlaybookStatus.SUFFICIENT, PlaybookStatus.COMPLETE]:
                return False
        
        return True
    
    def get_next_recommended_playbook(self) -> Optional[PlaybookType]:
        """Get the next recommended playbook to work on."""
        available = self.state.get_available_playbooks()
        if not available:
            return None
        
        # Sort by priority (HIGH first) and progress (least progress first)
        def sort_key(playbook_type):
            state = self.state.playbooks[playbook_type]
            priority_weight = {
                PlaybookPriority.HIGH: 4,
                PlaybookPriority.MEDIUM_HIGH: 3,
                PlaybookPriority.MEDIUM: 2,
                PlaybookPriority.MEDIUM_LOW: 1
            }[state.priority]
            return (priority_weight, -state.progress)  # Negative progress for ascending order
        
        return sorted(available, key=sort_key, reverse=True)[0]
    
    def update_playbook_progress(self, playbook_type: PlaybookType, progress: float, artifacts: Dict[str, Any] = None):
        """Update progress for a specific playbook and propagate changes."""
        state = self.state.playbooks[playbook_type]
        old_progress = state.progress
        state.progress = progress
        state.last_updated = datetime.now()
        
        if artifacts:
            state.generated_artifacts.update(artifacts)
        
        # Update status based on progress
        if progress >= 1.0:
            state.status = PlaybookStatus.COMPLETE
        elif progress >= 0.8:
            state.status = PlaybookStatus.SUFFICIENT
        elif progress > 0:
            state.status = PlaybookStatus.IN_PROGRESS
        
        # Check if this unblocks other playbooks
        self._update_dependencies(playbook_type)
        
        # Update shared knowledge if significant progress
        if progress >= 0.5 and old_progress < 0.5:
            self._extract_shared_knowledge(playbook_type, artifacts or {})
        
        # Update overall progress
        self._update_overall_progress()
    
    def _update_dependencies(self, updated_playbook: PlaybookType):
        """Update dependency status for all playbooks after one is updated."""
        for playbook_type in self.state.playbooks:
            self.state.playbooks[playbook_type].dependencies_met = self._check_dependencies_met(playbook_type)
    
    def _extract_shared_knowledge(self, playbook_type: PlaybookType, artifacts: Dict[str, Any]):
        """Extract knowledge from playbook artifacts to shared knowledge base."""
        if playbook_type == PlaybookType.VISION_OPPORTUNITY:
            if 'vision_statement' in artifacts:
                self.state.update_shared_knowledge('company_info.vision', artifacts['vision_statement'], playbook_type)
            if 'tam_calculation' in artifacts:
                self.state.update_shared_knowledge('target_market.tam', artifacts['tam_calculation'], playbook_type)
        
        elif playbook_type == PlaybookType.CUSTOMER_DISCOVERY:
            if 'customer_personas' in artifacts:
                self.state.update_shared_knowledge('target_market.personas', artifacts['customer_personas'], playbook_type)
            if 'pricing_insights' in artifacts:
                self.state.update_shared_knowledge('financial_data.pricing_insights', artifacts['pricing_insights'], playbook_type)
        
        elif playbook_type == PlaybookType.BUSINESS_MODEL:
            if 'revenue_model' in artifacts:
                self.state.update_shared_knowledge('financial_data.revenue_model', artifacts['revenue_model'], playbook_type)
            if 'unit_economics' in artifacts:
                self.state.update_shared_knowledge('financial_data.unit_economics', artifacts['unit_economics'], playbook_type)
        
        elif playbook_type == PlaybookType.PRODUCT_STRATEGY:
            if 'product_roadmap' in artifacts:
                self.state.update_shared_knowledge('product_details.roadmap', artifacts['product_roadmap'], playbook_type)
            if 'feature_prioritization' in artifacts:
                self.state.update_shared_knowledge('product_details.features', artifacts['feature_prioritization'], playbook_type)
        
        # Add more knowledge extraction rules for other playbooks...
    
    def _update_overall_progress(self):
        """Calculate and update overall progress across all playbooks."""
        if not self.state.playbooks:
            self.state.overall_progress = 0.0
            return
        
        total_weighted_progress = 0.0
        total_weight = 0.0
        
        weight_map = {
            PlaybookPriority.HIGH: 4.0,
            PlaybookPriority.MEDIUM_HIGH: 3.0,
            PlaybookPriority.MEDIUM: 2.0,
            PlaybookPriority.MEDIUM_LOW: 1.0
        }
        
        for state in self.state.playbooks.values():
            weight = weight_map[state.priority]
            total_weighted_progress += state.progress * weight
            total_weight += weight
        
        self.state.overall_progress = total_weighted_progress / total_weight if total_weight > 0 else 0.0
    
    def process_pending_updates(self):
        """Process all pending cross-playbook updates."""
        for update in self.state.pending_updates:
            if not update.propagated:
                self._propagate_update(update)
                update.propagated = True
        
        # Clear processed updates
        self.state.pending_updates = [u for u in self.state.pending_updates if not u.propagated]
    
    def _propagate_update(self, update: CrossPlaybookUpdate):
        """Propagate an update to affected playbooks."""
        for affected_playbook in update.affected_playbooks:
            # Find the relevant agent and notify it
            if affected_playbook in self.playbook_agents:
                agent = self.playbook_agents[affected_playbook]
                message = AgentCoordinationMessage(
                    from_agent=f"{update.source_playbook.value}_agent",
                    to_agent=f"{affected_playbook.value}_agent",
                    message_type="update",
                    content={
                        "update_type": update.update_type,
                        "changes": update.changes,
                        "source": update.source_playbook.value
                    },
                    priority=8
                )
                self.message_queue.append(message)
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get a comprehensive status summary."""
        return {
            "overall_progress": self.state.overall_progress,
            "active_playbook": self.state.active_playbook.value if self.state.active_playbook else None,
            "playbook_statuses": {
                pb_type.value: {
                    "status": state.status.value,
                    "progress": state.progress,
                    "priority": state.priority.value,
                    "dependencies_met": state.dependencies_met,
                    "blocked_by": [pb.value for pb in state.blocked_by]
                }
                for pb_type, state in self.state.playbooks.items()
            },
            "available_playbooks": [pb.value for pb in self.state.get_available_playbooks()],
            "pending_updates": len(self.state.pending_updates),
            "shared_knowledge_items": len(self.state.shared_knowledge.update_history)
        }
    
    def save_state(self, filepath: str = "multi_playbook_state.json"):
        """Save the current state to a file."""
        state_dict = self.state.dict()
        with open(filepath, 'w') as f:
            json.dump(state_dict, f, indent=2, default=str)
    
    def load_state(self, filepath: str = "multi_playbook_state.json"):
        """Load state from a file."""
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                state_dict = json.load(f)
            self.state = MultiPlaybookWorkflowState(**state_dict)
            return True
        return False 