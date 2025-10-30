"""
Main workflow orchestration for the Vision & Opportunity Playbook.
Coordinates agents, manages state, and controls the overall flow.
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

from models import (
    WorkflowState, Question, QuestionCategory, Task, TaskStatus,
    VisionStatement, TAMResult, QualityAssessment
)
from agents import (
    QuestionGeneratorAgent, WorkflowCoordinatorAgent, VisionStatementAgent,
    TAMCalculatorAgent, MarketTimingAgent, ExitStrategyAgent
)
from ui import VisionOpportunityUI


class VisionOpportunityWorkflow:
    """Main workflow orchestrator for the Vision & Opportunity Playbook."""
    
    def __init__(self):
        self.ui = VisionOpportunityUI()
        self.workflow_state = WorkflowState()
        self.coordinator = WorkflowCoordinatorAgent()
        self.question_generator = QuestionGeneratorAgent()
        
        # Cost limits
        self.cost_limits = {
            "max_tokens": 20000,
            "max_api_calls": 50,
            "max_computation_time": 300  # 5 minutes
        }
        
        # Track start time
        self.start_time = datetime.now()
    
    def run(self):
        """Main workflow execution."""
        try:
            # Welcome screen
            self.ui.show_welcome()
            
            # Information gathering phase
            self._information_gathering_phase()
            
            # Analysis and synthesis phase
            if self.workflow_state.completion_monitor.enough_info_reached:
                self._analysis_synthesis_phase()
            
            # Final summary
            self._final_summary_phase()
            
        except KeyboardInterrupt:
            self.ui.show_error("Workflow interrupted by user")
        except Exception as e:
            self.ui.show_error(f"An error occurred: {str(e)}")
        finally:
            self._cleanup()
    
    def _information_gathering_phase(self):
        """Phase 1: Interactive information gathering."""
        self.ui.show_status("Starting information gathering phase...")
        
        while not self.workflow_state.completion_monitor.enough_info_reached:
            # Show current progress
            self.ui.show_progress(self.workflow_state)
            
            # Check cost limits
            self._check_cost_limits()
            
            # Generate next question
            try:
                question = self.question_generator.generate_question(self.workflow_state)
                self.workflow_state.current_question = question
                
            except Exception as e:
                self.ui.show_error(f"Failed to generate question: {str(e)}")
                break
            
            # Ask question and get response
            response = self.ui.ask_question(question, self.workflow_state)
            
            if response is None:  # User quit
                break
            elif response == 'skip':  # User skipped
                self.workflow_state.completion_monitor.enough_info_reached = True
                break
            elif response.strip():  # Valid response
                # Add response to workflow state
                question_id = f"q_{self.workflow_state.questions_asked + 1}"
                self.workflow_state.add_response(question_id, response, question.category)
                
                # Update cost metrics
                self._update_cost_metrics(
                    tokens=len(response.split()) * 2,  # Rough token estimate
                    computation_time=1.0,
                    api_calls=1
                )
            
            # Clear screen for next question
            self.ui.print_separator()
            
        self.ui.show_status("Information gathering phase complete")
    
    def _analysis_synthesis_phase(self):
        """Phase 2: Analysis and synthesis using AI agents."""
        self.ui.show_status("Starting analysis and synthesis phase...")
        
        # Determine next action
        next_action = self.coordinator.determine_next_action(self.workflow_state)
        
        if next_action == "PARALLEL_STEP":
            self._execute_parallel_tasks()
        elif next_action == "SERIAL_STEP":
            self._execute_serial_tasks()
    
    def _execute_parallel_tasks(self):
        """Execute tasks that can run in parallel."""
        parallel_tasks = self.coordinator.create_parallel_tasks(self.workflow_state)
        
        if not parallel_tasks:
            return
        
        self.ui.show_status("Executing parallel analysis tasks...")
        
        # Show task execution progress
        results = self.ui.show_task_execution(parallel_tasks)
        
        # Execute tasks with actual agents
        for task in parallel_tasks:
            try:
                if task.task_id == "vision_statement":
                    agent = self.coordinator.agents["vision_statement"]
                    result = agent.generate_vision_statement(self.workflow_state)
                    self.workflow_state.generated_components["vision_statement"] = result
                    
                    # Show result
                    self.ui.show_vision_statement(result)
                    
                elif task.task_id == "tam_calculation":
                    agent = self.coordinator.agents["tam_calculator"]
                    result = agent.calculate_tam(self.workflow_state)
                    self.workflow_state.generated_components["tam_calculation"] = result
                    
                    # Show result
                    self.ui.show_tam_analysis(result)
                    
                elif task.task_id == "timing_analysis":
                    agent = self.coordinator.agents["market_timing"]
                    result = agent.analyze_timing(self.workflow_state)
                    self.workflow_state.generated_components["timing_analysis"] = result
                
                # Update cost metrics
                self._update_cost_metrics(
                    tokens=agent.cost_metrics.tokens_used,
                    computation_time=agent.cost_metrics.computation_time,
                    api_calls=agent.cost_metrics.api_calls
                )
                
            except Exception as e:
                self.ui.show_error(f"Failed to execute task {task.name}: {str(e)}")
        
        # Execute serial tasks if any
        self._execute_serial_tasks()
    
    def _execute_serial_tasks(self):
        """Execute tasks that must run sequentially."""
        serial_tasks = self.coordinator.create_serial_tasks(self.workflow_state)
        
        for task in serial_tasks:
            try:
                self.ui.show_status(f"Executing {task.name}...")
                
                if task.task_id == "exit_strategy":
                    agent = self.coordinator.agents["exit_strategy"]
                    result = agent.develop_exit_strategy(self.workflow_state)
                    self.workflow_state.generated_components["exit_strategy"] = result
                
                # Update cost metrics
                self._update_cost_metrics(
                    tokens=agent.cost_metrics.tokens_used,
                    computation_time=agent.cost_metrics.computation_time,
                    api_calls=agent.cost_metrics.api_calls
                )
                
            except Exception as e:
                self.ui.show_error(f"Failed to execute task {task.name}: {str(e)}")
    
    def _final_summary_phase(self):
        """Phase 3: Final summary and export."""
        self.ui.show_status("Generating final summary...")
        
        # Show final summary
        self.ui.show_final_summary(self.workflow_state)
        
        # Export results
        self._export_results()
    
    def _export_results(self):
        """Export workflow results to markdown file."""
        try:
            output_file = "vision_opportunity_assessment.md"
            
            # Generate markdown content
            markdown_content = self._generate_markdown_report()
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            self.ui.show_status(f"Results exported to {output_file}")
            
        except Exception as e:
            self.ui.show_error(f"Failed to export results: {str(e)}")
    
    def _generate_markdown_report(self) -> str:
        """Generate markdown report from workflow results."""
        report = f"""# Vision & Opportunity Assessment

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Executive Summary

This assessment was completed using the AI-Powered Startup Framework, analyzing {len(self.workflow_state.user_responses)} responses across {len(self.workflow_state.completion_monitor.categories)} categories with {self.workflow_state.completion_monitor.overall_completion:.0%} completion.

## Vision Statement

"""
        
        # Add vision statement if available
        if "vision_statement" in self.workflow_state.generated_components:
            vision = self.workflow_state.generated_components["vision_statement"]
            report += f"**Recommended Vision:** {vision.recommended_choice}\n\n"
            report += f"**Reasoning:** {vision.reasoning}\n\n"
            
            report += "### Alternative Variations:\n\n"
            for i, variation in enumerate(vision.variations, 1):
                report += f"{i}. **{variation.tone.title()}:** {variation.statement}\n"
                report += f"   - *{variation.use_case}*\n\n"
        
        # Add TAM analysis if available
        if "tam_calculation" in self.workflow_state.generated_components:
            tam = self.workflow_state.generated_components["tam_calculation"]
            report += f"""## Total Addressable Market

### TAM Range
- **Conservative:** ${tam.final_range.conservative:,.0f}
- **Recommended:** ${tam.final_range.recommended:,.0f}
- **Optimistic:** ${tam.final_range.optimistic:,.0f}

### Calculation Methods
"""
            
            for method_name, calc in tam.calculations.items():
                report += f"**{method_name.replace('_', ' ').title()}:**\n"
                report += f"- Market Size: ${calc.market_size:,.0f}\n"
                report += f"- Addressable Percentage: {calc.addressable_percentage:.1%}\n"
                report += f"- TAM Estimate: ${calc.tam_estimate:,.0f}\n"
                report += f"- Confidence Level: {calc.confidence_level:.0%}\n\n"
        
        # Add timing analysis if available
        if "timing_analysis" in self.workflow_state.generated_components:
            timing = self.workflow_state.generated_components["timing_analysis"]
            report += f"""## Market Timing Analysis

{timing['executive_summary']}

### Timing Scores
"""
            for factor, score in timing['timing_scores'].items():
                report += f"- {factor.replace('_', ' ').title()}: {score}/10\n"
            
            report += f"""
### Key Opportunities
"""
            for opportunity in timing['key_opportunities']:
                report += f"- {opportunity}\n"
        
        # Add exit strategy if available
        if "exit_strategy" in self.workflow_state.generated_components:
            exit_strategy = self.workflow_state.generated_components["exit_strategy"]
            report += f"""## Exit Strategy

**Primary Exit Scenario:** {exit_strategy['primary_exit_scenario']}

**Timeline:** {exit_strategy['timeline_considerations']}

### Value Creation Milestones
"""
            for milestone in exit_strategy['value_creation_milestones']:
                report += f"- {milestone}\n"
        
        # Add user responses
        report += f"""## User Responses Summary

Total questions answered: {len(self.workflow_state.user_responses)}

"""
        
        # Group responses by category
        for category in QuestionCategory:
            category_responses = [r for r in self.workflow_state.user_responses if r.category == category]
            if category_responses:
                report += f"### {category.value.replace('_', ' ').title()}\n\n"
                for i, response in enumerate(category_responses, 1):
                    report += f"{i}. {response.response}\n"
                report += "\n"
        
        # Add session metadata
        report += f"""## Session Metadata

- **Completion Level:** {self.workflow_state.completion_monitor.overall_completion:.0%}
- **Questions Asked:** {self.workflow_state.questions_asked}
- **Components Generated:** {len(self.workflow_state.generated_components)}
- **Total Tokens Used:** {self.workflow_state.cost_metrics.tokens_used:,}
- **Processing Time:** {self.workflow_state.cost_metrics.computation_time:.1f}s
- **API Calls:** {self.workflow_state.cost_metrics.api_calls}

## Next Steps

1. Review and refine your vision statement
2. Validate TAM calculations with market research
3. Develop detailed go-to-market strategy
4. Create investor pitch deck
5. Begin customer discovery interviews

---

*Generated by AI Startup Framework - Vision & Opportunity Playbook*
"""
        
        return report
    
    def _check_cost_limits(self):
        """Check if approaching cost limits and warn user."""
        current_cost = {
            "tokens": self.workflow_state.cost_metrics.tokens_used,
            "api_calls": self.workflow_state.cost_metrics.api_calls,
            "computation_time": self.workflow_state.cost_metrics.computation_time
        }
        
        # Check if approaching limits (80% threshold)
        warning_needed = False
        for metric, current in current_cost.items():
            limit = self.cost_limits.get(f"max_{metric}", 0)
            if limit > 0 and (current / limit) > 0.8:
                warning_needed = True
                break
        
        if warning_needed:
            self.ui.show_cost_warning(current_cost, self.cost_limits)
    
    def _update_cost_metrics(self, tokens: int, computation_time: float, api_calls: int):
        """Update cost metrics in workflow state."""
        self.workflow_state.cost_metrics.tokens_used += tokens
        self.workflow_state.cost_metrics.computation_time += computation_time
        self.workflow_state.cost_metrics.api_calls += api_calls
    
    def _cleanup(self):
        """Cleanup resources and finalize workflow."""
        self.workflow_state.cost_metrics.computation_time = (
            datetime.now() - self.start_time
        ).total_seconds()
        
        # Save workflow state for debugging
        try:
            with open("workflow_state.json", "w") as f:
                # Convert to dict for JSON serialization
                state_dict = {
                    "questions_asked": self.workflow_state.questions_asked,
                    "overall_completion": self.workflow_state.completion_monitor.overall_completion,
                    "responses_count": len(self.workflow_state.user_responses),
                    "components_generated": list(self.workflow_state.generated_components.keys()),
                    "cost_metrics": {
                        "tokens_used": self.workflow_state.cost_metrics.tokens_used,
                        "computation_time": self.workflow_state.cost_metrics.computation_time,
                        "api_calls": self.workflow_state.cost_metrics.api_calls
                    }
                }
                json.dump(state_dict, f, indent=2)
        except Exception:
            pass  # Ignore cleanup errors 