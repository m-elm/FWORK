"""
Agent implementations for the Vision & Opportunity Playbook workflow.
Each agent is responsible for specific tasks within the workflow.
"""

import random
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from models import (
    Question, QuestionCategory, WorkflowState, VisionStatement, VisionVariation,
    Citation, TAMResult, TAMCalculation, TAMRange, CostMetrics, Task, TaskStatus
)


class BaseAgent:
    """Base class for all agents in the workflow."""
    
    def __init__(self, name: str, cost_limits: Dict[str, int]):
        self.name = name
        self.cost_limits = cost_limits
        self.cost_metrics = CostMetrics(tokens_used=0, computation_time=0.0, api_calls=0)
    
    def track_cost(self, tokens: int, time_spent: float, api_calls: int = 1):
        """Track cost metrics for the agent."""
        self.cost_metrics.tokens_used += tokens
        self.cost_metrics.computation_time += time_spent
        self.cost_metrics.api_calls += api_calls
        
        # Check limits
        if self.cost_metrics.tokens_used > self.cost_limits.get("max_tokens", 5000):
            raise Exception(f"Token limit exceeded for {self.name}")
        if self.cost_metrics.api_calls > self.cost_limits.get("max_api_calls", 10):
            raise Exception(f"API call limit exceeded for {self.name}")


class QuestionGeneratorAgent(BaseAgent):
    """Agent responsible for generating questions based on current workflow state."""
    
    def __init__(self):
        super().__init__("QuestionGenerator", {"max_tokens": 1000, "max_api_calls": 20})
        self.question_templates = {
            QuestionCategory.PROBLEM_CLARITY: [
                "What specific problem are you trying to solve?",
                "Who is your target customer experiencing this problem?",
                "How painful is this problem for your target audience?",
                "What are people currently doing to solve this problem?",
                "How much does this problem cost your target customers?",
            ],
            QuestionCategory.MARKET_CONTEXT: [
                "What industry or market are you targeting?",
                "What trends are driving demand for your solution?",
                "Who are your main competitors?",
                "What regulations might affect your market?",
                "How is technology changing your target market?",
            ],
            QuestionCategory.SOLUTION_UNIQUENESS: [
                "What makes your solution different from existing options?",
                "What's your unique value proposition?",
                "What key benefits do you provide that others don't?",
                "What's your competitive advantage?",
                "Why would customers choose you over alternatives?",
            ],
            QuestionCategory.SCALE_POTENTIAL: [
                "How large is your target market?",
                "What's your pricing strategy?",
                "How much would customers pay for your solution?",
                "How many potential customers exist?",
                "What's the growth potential of your market?",
            ],
            QuestionCategory.EXECUTION_READINESS: [
                "What's your background and relevant experience?",
                "What resources do you currently have?",
                "What's your timeline for launch?",
                "What are your biggest risks?",
                "What do you need to get started?",
            ],
        }
    
    def generate_question(self, workflow_state: WorkflowState) -> Question:
        """Generate the next most appropriate question based on workflow state."""
        start_time = time.time()
        
        # Find the category with lowest progress
        target_category = min(
            workflow_state.completion_monitor.categories.keys(),
            key=lambda cat: workflow_state.completion_monitor.categories[cat].progress
        )
        
        # Select a question from that category
        available_questions = self.question_templates[target_category]
        
        # Avoid repeating questions (simplified logic)
        asked_questions = [resp.response for resp in workflow_state.user_responses 
                          if resp.category == target_category]
        
        question_text = random.choice(available_questions)
        
        # Mock question generation logic
        question = Question(
            question=question_text,
            category=target_category,
            rationale=f"This helps us understand {target_category.value} better",
            completion_impact=0.2,
            skip_option=workflow_state.completion_monitor.skip_available,
            follow_up_hints=["Be specific", "Provide examples", "Quantify if possible"]
        )
        
        # Track cost
        self.track_cost(tokens=50, time_spent=time.time() - start_time)
        
        return question


class VisionStatementAgent(BaseAgent):
    """Agent responsible for generating vision statements."""
    
    def __init__(self):
        super().__init__("VisionStatement", {"max_tokens": 2000, "max_api_calls": 5})
    
    def generate_vision_statement(self, workflow_state: WorkflowState) -> VisionStatement:
        """Generate vision statement variations based on collected data."""
        start_time = time.time()
        
        # Extract key information from responses
        problem_responses = [r for r in workflow_state.user_responses 
                           if r.category == QuestionCategory.PROBLEM_CLARITY]
        market_responses = [r for r in workflow_state.user_responses 
                          if r.category == QuestionCategory.MARKET_CONTEXT]
        solution_responses = [r for r in workflow_state.user_responses 
                            if r.category == QuestionCategory.SOLUTION_UNIQUENESS]
        
        # Mock vision statement generation
        base_problem = "solve complex challenges" if problem_responses else "create value"
        base_audience = "businesses" if market_responses else "users"
        base_approach = "innovative technology" if solution_responses else "smart solutions"
        
        variations = [
            VisionVariation(
                statement=f"We {base_problem} for {base_audience} by {base_approach} to transform their future",
                tone="ambitious",
                emotional_appeal=9,
                clarity_score=7,
                differentiation_score=8,
                use_case="For investor presentations and team inspiration"
            ),
            VisionVariation(
                statement=f"We help {base_audience} {base_problem} through {base_approach} efficiently",
                tone="practical",
                emotional_appeal=6,
                clarity_score=9,
                differentiation_score=6,
                use_case="For customer communications and marketing"
            ),
            VisionVariation(
                statement=f"We revolutionize how {base_audience} {base_problem} with {base_approach}",
                tone="disruptive",
                emotional_appeal=8,
                clarity_score=8,
                differentiation_score=9,
                use_case="For disrupting markets and attracting early adopters"
            ),
        ]
        
        # Mock citations
        citations = [
            Citation(
                source="Market Research Report 2024",
                date_retrieved=datetime.now() - timedelta(days=30),
                relevance_score=0.8,
                content_snippet="Market trends show increasing demand...",
                freshness_flag="current"
            )
        ]
        
        vision_statement = VisionStatement(
            variations=variations,
            recommended_choice=variations[0].statement,
            reasoning="The ambitious tone aligns with startup culture and investment appeal",
            citations=citations
        )
        
        # Track cost
        self.track_cost(tokens=300, time_spent=time.time() - start_time)
        
        return vision_statement


class TAMCalculatorAgent(BaseAgent):
    """Agent responsible for calculating Total Addressable Market."""
    
    def __init__(self):
        super().__init__("TAMCalculator", {"max_tokens": 4000, "max_api_calls": 15})
    
    def calculate_tam(self, workflow_state: WorkflowState) -> TAMResult:
        """Calculate TAM using multiple methodologies."""
        start_time = time.time()
        
        # Extract relevant responses
        market_responses = [r for r in workflow_state.user_responses 
                          if r.category == QuestionCategory.MARKET_CONTEXT]
        scale_responses = [r for r in workflow_state.user_responses 
                         if r.category == QuestionCategory.SCALE_POTENTIAL]
        
        # Mock TAM calculations
        base_market_size = 1000000000  # $1B base market
        if market_responses:
            base_market_size *= 1.5  # Increase if we have market context
        
        top_down = TAMCalculation(
            market_size=base_market_size,
            addressable_percentage=0.1,
            tam_estimate=base_market_size * 0.1,
            confidence_level=0.7,
            assumptions=[
                "Market research data from 2024",
                "Assuming 10% market penetration",
                "Based on similar industry benchmarks"
            ],
            calculation_steps=[
                "Identified total market size",
                "Applied addressable market filter",
                "Calculated final TAM estimate"
            ]
        )
        
        # Mock bottom-up calculation
        target_customers = 10000
        arpu = 5000
        
        bottom_up = TAMCalculation(
            market_size=target_customers * arpu,
            addressable_percentage=1.0,
            tam_estimate=target_customers * arpu,
            confidence_level=0.8,
            assumptions=[
                "10,000 target customers identified",
                "$5,000 average revenue per user",
                "Based on customer interview data"
            ],
            calculation_steps=[
                "Counted addressable customers",
                "Estimated average revenue per user",
                "Multiplied for total TAM"
            ]
        )
        
        # Calculate final range
        conservative = min(top_down.tam_estimate, bottom_up.tam_estimate) * 0.7
        optimistic = max(top_down.tam_estimate, bottom_up.tam_estimate) * 1.3
        recommended = (top_down.tam_estimate + bottom_up.tam_estimate) / 2
        
        final_range = TAMRange(
            conservative=conservative,
            optimistic=optimistic,
            recommended=recommended
        )
        
        # Mock citations
        citations = [
            Citation(
                source="Industry Analysis Report 2024",
                date_retrieved=datetime.now() - timedelta(days=15),
                relevance_score=0.9,
                content_snippet="Market size estimated at $1B with 15% growth",
                freshness_flag="current"
            )
        ]
        
        tam_result = TAMResult(
            calculations={
                "top_down": top_down,
                "bottom_up": bottom_up
            },
            final_range=final_range,
            validation_checks=[
                "Compared with industry benchmarks",
                "Cross-validated with competitor analysis",
                "Checked against similar startups"
            ],
            citations=citations,
            cost_metrics=CostMetrics(
                tokens_used=400,
                computation_time=time.time() - start_time,
                api_calls=3
            )
        )
        
        # Track cost
        self.track_cost(tokens=400, time_spent=time.time() - start_time, api_calls=3)
        
        return tam_result


class MarketTimingAgent(BaseAgent):
    """Agent responsible for market timing analysis."""
    
    def __init__(self):
        super().__init__("MarketTiming", {"max_tokens": 3000, "max_api_calls": 10})
    
    def analyze_timing(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Analyze market timing using the TIMING framework."""
        start_time = time.time()
        
        # Mock timing analysis
        timing_analysis = {
            "executive_summary": "Market timing shows strong opportunity with favorable trends",
            "timing_scores": {
                "technology_enablers": 8,
                "industry_trends": 7,
                "market_maturity": 6,
                "infrastructure": 7,
                "narrative_momentum": 8,
                "solution_gaps": 9
            },
            "key_opportunities": [
                "Emerging technology makes solution feasible",
                "Industry consolidation creates market gaps",
                "Regulatory changes favor new entrants"
            ],
            "timing_risks": [
                "Market may be oversaturated",
                "Technology adoption slower than expected"
            ],
            "optimal_entry_window": "Next 6-12 months",
            "recommended_strategies": [
                "Move quickly to establish market position",
                "Focus on early adopters",
                "Build partnerships with industry leaders"
            ]
        }
        
        # Track cost
        self.track_cost(tokens=250, time_spent=time.time() - start_time, api_calls=2)
        
        return timing_analysis


class ExitStrategyAgent(BaseAgent):
    """Agent responsible for exit strategy development."""
    
    def __init__(self):
        super().__init__("ExitStrategy", {"max_tokens": 2000, "max_api_calls": 8})
    
    def develop_exit_strategy(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Develop exit strategy considerations."""
        start_time = time.time()
        
        # Mock exit strategy
        exit_strategy = {
            "primary_exit_scenario": "Strategic acquisition by industry leader",
            "secondary_exit_options": [
                "Private equity acquisition",
                "IPO after reaching $100M revenue",
                "Management buyout"
            ],
            "value_creation_milestones": [
                "Product-market fit within 18 months",
                "$10M ARR within 3 years",
                "Market leadership position within 5 years"
            ],
            "timeline_considerations": "3-7 years to exit depending on growth rate",
            "strategic_implications": [
                "Focus on scalable business model",
                "Build strong IP portfolio",
                "Establish key partnerships"
            ],
            "potential_acquirers": [
                "Large tech companies in adjacent markets",
                "Industry incumbents seeking innovation",
                "Private equity firms focused on growth"
            ]
        }
        
        # Track cost
        self.track_cost(tokens=200, time_spent=time.time() - start_time, api_calls=1)
        
        return exit_strategy


class WorkflowCoordinatorAgent(BaseAgent):
    """Agent responsible for coordinating the overall workflow."""
    
    def __init__(self):
        super().__init__("WorkflowCoordinator", {"max_tokens": 1500, "max_api_calls": 30})
        self.agents = {
            "question_generator": QuestionGeneratorAgent(),
            "vision_statement": VisionStatementAgent(),
            "tam_calculator": TAMCalculatorAgent(),
            "market_timing": MarketTimingAgent(),
            "exit_strategy": ExitStrategyAgent(),
        }
    
    def determine_next_action(self, workflow_state: WorkflowState) -> str:
        """Determine the next action based on workflow state."""
        if workflow_state.completion_monitor.enough_info_reached:
            if not workflow_state.generated_components:
                return "PARALLEL_STEP"
            else:
                return "COMPLETE"
        else:
            return "ASK_QUESTION"
    
    def create_parallel_tasks(self, workflow_state: WorkflowState) -> List[Task]:
        """Create parallel tasks for component generation."""
        tasks = []
        
        # Vision statement and problem brief can run in parallel
        tasks.append(Task(
            task_id="vision_statement",
            name="Generate Vision Statement",
            agent="vision_statement",
            estimated_time=30,
            prerequisites=["problem_clarity_sufficient"]
        ))
        
        # TAM calculation and timing analysis can run in parallel
        tasks.append(Task(
            task_id="tam_calculation",
            name="Calculate TAM",
            agent="tam_calculator",
            estimated_time=45,
            prerequisites=["market_context_sufficient"]
        ))
        
        tasks.append(Task(
            task_id="timing_analysis",
            name="Analyze Market Timing",
            agent="market_timing",
            estimated_time=35,
            prerequisites=["market_context_sufficient"]
        ))
        
        return tasks
    
    def create_serial_tasks(self, workflow_state: WorkflowState) -> List[Task]:
        """Create serial tasks that depend on other tasks."""
        tasks = []
        
        # Exit strategy depends on TAM calculation
        tasks.append(Task(
            task_id="exit_strategy",
            name="Develop Exit Strategy",
            agent="exit_strategy",
            estimated_time=25,
            prerequisites=["tam_calculation_complete"]
        ))
        
        return tasks
    
    def execute_task(self, task: Task, workflow_state: WorkflowState) -> Any:
        """Execute a specific task using the appropriate agent."""
        agent = self.agents.get(task.agent)
        if not agent:
            raise ValueError(f"Unknown agent: {task.agent}")
        
        task.status = TaskStatus.IN_PROGRESS
        task.start_time = datetime.now()
        
        try:
            if task.task_id == "vision_statement":
                result = agent.generate_vision_statement(workflow_state)
            elif task.task_id == "tam_calculation":
                result = agent.calculate_tam(workflow_state)
            elif task.task_id == "timing_analysis":
                result = agent.analyze_timing(workflow_state)
            elif task.task_id == "exit_strategy":
                result = agent.develop_exit_strategy(workflow_state)
            else:
                raise ValueError(f"Unknown task: {task.task_id}")
            
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.end_time = datetime.now()
            
            return result
            
        except Exception as e:
            task.error = str(e)
            task.status = TaskStatus.FAILED
            task.end_time = datetime.now()
            raise e 