"""
Data models and schemas for the Vision & Opportunity Playbook workflow.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class QuestionCategory(str, Enum):
    PROBLEM_CLARITY = "problem_clarity"
    MARKET_CONTEXT = "market_context"
    SOLUTION_UNIQUENESS = "solution_uniqueness"
    SCALE_POTENTIAL = "scale_potential"
    EXECUTION_READINESS = "execution_readiness"


class CompletionStatus(str, Enum):
    COMPLETE = "complete"
    IN_PROGRESS = "in_progress"
    NEEDS_INPUT = "needs_input"
    SUFFICIENT = "sufficient"


class CategoryProgress(BaseModel):
    progress: float = Field(ge=0, le=1, description="Progress percentage (0-1)")
    status: CompletionStatus = Field(description="Current status of the category")


class CompletionMonitor(BaseModel):
    categories: Dict[QuestionCategory, CategoryProgress] = Field(
        description="Progress for each question category"
    )
    overall_completion: float = Field(ge=0, le=1, description="Overall completion percentage")
    enough_info_reached: bool = Field(description="Whether enough information has been gathered")
    missing_critical_info: List[str] = Field(description="List of missing critical information")
    skip_available: bool = Field(description="Whether user can skip remaining questions")


class Question(BaseModel):
    question: str = Field(description="The question to ask the user")
    category: QuestionCategory = Field(description="Category this question belongs to")
    rationale: str = Field(description="Why this question is important")
    completion_impact: float = Field(ge=0, le=1, description="Impact on completion percentage")
    skip_option: bool = Field(description="Whether skip option should be offered")
    follow_up_hints: List[str] = Field(description="Potential follow-up topics")


class UserResponse(BaseModel):
    question_id: str = Field(description="Unique identifier for the question")
    response: str = Field(description="User's response to the question")
    timestamp: datetime = Field(default_factory=datetime.now)
    category: QuestionCategory = Field(description="Category of the question")


class Citation(BaseModel):
    source: str = Field(description="Source of the information")
    date_retrieved: datetime = Field(description="When the information was retrieved")
    relevance_score: float = Field(ge=0, le=1, description="Relevance score of the source")
    content_snippet: Optional[str] = Field(description="Snippet of relevant content")
    freshness_flag: str = Field(description="current|stale|outdated")


class VisionVariation(BaseModel):
    statement: str = Field(min_length=10, max_length=200, description="Vision statement")
    tone: str = Field(description="Tone of the statement: ambitious|practical|disruptive")
    emotional_appeal: int = Field(ge=1, le=10, description="Emotional appeal score")
    clarity_score: int = Field(ge=1, le=10, description="Clarity score")
    differentiation_score: int = Field(ge=1, le=10, description="Differentiation score")
    use_case: str = Field(description="Recommended use case for this variation")


class VisionStatement(BaseModel):
    variations: List[VisionVariation] = Field(min_length=3, max_length=3)
    recommended_choice: str = Field(description="Recommended variation")
    reasoning: str = Field(description="Reasoning for the recommendation")
    citations: List[Citation] = Field(description="Supporting citations")


class TAMCalculation(BaseModel):
    market_size: float = Field(description="Total market size")
    addressable_percentage: float = Field(description="Addressable market percentage")
    tam_estimate: float = Field(description="TAM estimate")
    confidence_level: float = Field(ge=0, le=1, description="Confidence in the calculation")
    assumptions: List[str] = Field(description="Key assumptions made")
    calculation_steps: List[str] = Field(description="Steps taken in calculation")


class TAMRange(BaseModel):
    conservative: float = Field(description="Conservative TAM estimate")
    optimistic: float = Field(description="Optimistic TAM estimate")
    recommended: float = Field(description="Recommended TAM estimate")


class CostMetrics(BaseModel):
    tokens_used: int = Field(description="Total tokens used")
    computation_time: float = Field(description="Computation time in seconds")
    api_calls: int = Field(description="Number of API calls made")


class TAMResult(BaseModel):
    calculations: Dict[str, TAMCalculation] = Field(description="Top-down and bottom-up calculations")
    final_range: TAMRange = Field(description="Final TAM range")
    validation_checks: List[str] = Field(description="Validation checks performed")
    citations: List[Citation] = Field(description="Supporting citations")
    cost_metrics: CostMetrics = Field(description="Cost tracking metrics")


class QualityIssue(BaseModel):
    issue: str = Field(description="Description of the quality issue")
    severity: str = Field(description="low|medium|high")
    component: str = Field(description="Component affected")
    suggestion: str = Field(description="Suggestion for improvement")


class ComponentScore(BaseModel):
    clarity: int = Field(ge=1, le=10, description="Clarity score")
    completeness: int = Field(ge=1, le=10, description="Completeness score")
    consistency: int = Field(ge=1, le=10, description="Consistency score")
    credibility: int = Field(ge=1, le=10, description="Credibility score")
    compelling: int = Field(ge=1, le=10, description="How compelling it is")
    specific_issues: List[str] = Field(description="Specific issues identified")
    improvement_suggestions: List[str] = Field(description="Suggestions for improvement")


class CitationHealth(BaseModel):
    total_citations: int = Field(description="Total number of citations")
    fresh_citations: int = Field(description="Number of fresh citations")
    stale_citations: int = Field(description="Number of stale citations")
    outdated_citations: int = Field(description="Number of outdated citations")


class QualityAssessment(BaseModel):
    component_scores: Dict[str, ComponentScore] = Field(description="Scores for each component")
    overall_quality: int = Field(ge=1, le=10, description="Overall quality score")
    approval_status: str = Field(description="approved|needs_revision|rejected")
    priority_improvements: List[str] = Field(description="Priority improvements needed")
    citations_health: CitationHealth = Field(description="Health of citations")


class WorkflowState(BaseModel):
    """Represents the current state of the workflow."""
    user_responses: List[UserResponse] = Field(default_factory=list)
    completion_monitor: CompletionMonitor = Field(default_factory=lambda: CompletionMonitor(
        categories={
            QuestionCategory.PROBLEM_CLARITY: CategoryProgress(progress=0.0, status=CompletionStatus.NEEDS_INPUT),
            QuestionCategory.MARKET_CONTEXT: CategoryProgress(progress=0.0, status=CompletionStatus.NEEDS_INPUT),
            QuestionCategory.SOLUTION_UNIQUENESS: CategoryProgress(progress=0.0, status=CompletionStatus.NEEDS_INPUT),
            QuestionCategory.SCALE_POTENTIAL: CategoryProgress(progress=0.0, status=CompletionStatus.NEEDS_INPUT),
            QuestionCategory.EXECUTION_READINESS: CategoryProgress(progress=0.0, status=CompletionStatus.NEEDS_INPUT),
        },
        overall_completion=0.0,
        enough_info_reached=False,
        missing_critical_info=[],
        skip_available=False
    ))
    questions_asked: int = Field(default=0)
    current_question: Optional[Question] = Field(default=None)
    generated_components: Dict[str, Any] = Field(default_factory=dict)
    cost_metrics: CostMetrics = Field(default_factory=lambda: CostMetrics(
        tokens_used=0, computation_time=0.0, api_calls=0
    ))
    
    def add_response(self, question_id: str, response: str, category: QuestionCategory):
        """Add a user response to the workflow state."""
        user_response = UserResponse(
            question_id=question_id,
            response=response,
            category=category
        )
        self.user_responses.append(user_response)
        self.questions_asked += 1
        self._update_completion_monitor()
    
    def _update_completion_monitor(self):
        """Update the completion monitor based on current responses."""
        # Count responses per category
        category_counts = {}
        for response in self.user_responses:
            category = response.category
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Update category progress (simplified logic)
        for category, progress in self.completion_monitor.categories.items():
            count = category_counts.get(category, 0)
            progress.progress = min(count * 0.25, 1.0)  # Each response adds 25% to category
            if progress.progress >= 0.8:
                progress.status = CompletionStatus.COMPLETE
            elif progress.progress >= 0.5:
                progress.status = CompletionStatus.SUFFICIENT
            elif progress.progress > 0:
                progress.status = CompletionStatus.IN_PROGRESS
            else:
                progress.status = CompletionStatus.NEEDS_INPUT
        
        # Update overall completion
        total_progress = sum(cat.progress for cat in self.completion_monitor.categories.values())
        self.completion_monitor.overall_completion = total_progress / len(self.completion_monitor.categories)
        
        # Check if enough info is reached
        self.completion_monitor.enough_info_reached = (
            self.completion_monitor.overall_completion >= 0.8 or self.questions_asked >= 8
        )
        
        # Update skip availability
        self.completion_monitor.skip_available = self.questions_asked >= 6
        
        # Update missing critical info
        self.completion_monitor.missing_critical_info = [
            f"Need more information about {category.value}"
            for category, progress in self.completion_monitor.categories.items()
            if progress.progress < 0.5
        ]


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    task_id: str = Field(description="Unique task identifier")
    name: str = Field(description="Task name")
    agent: str = Field(description="Agent responsible for the task")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    estimated_time: int = Field(description="Estimated time in seconds")
    prerequisites: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    result: Optional[Any] = Field(default=None)
    error: Optional[str] = Field(default=None)
    start_time: Optional[datetime] = Field(default=None)
    end_time: Optional[datetime] = Field(default=None) 