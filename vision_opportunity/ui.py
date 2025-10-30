"""
Console UI components for the Vision & Opportunity Playbook workflow.
Uses Rich library for beautiful terminal interface.
"""

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.layout import Layout
from rich.live import Live
from rich.align import Align
from rich.columns import Columns
from rich.rule import Rule
from rich.tree import Tree
from rich.status import Status
from typing import Dict, List, Optional, Any
import time

from models import (
    WorkflowState, Question, QuestionCategory, CompletionStatus,
    VisionStatement, TAMResult, Task, TaskStatus
)


class VisionOpportunityUI:
    """Main UI class for the Vision & Opportunity Playbook workflow."""
    
    def __init__(self):
        self.console = Console()
        self.progress_colors = {
            CompletionStatus.COMPLETE: "green",
            CompletionStatus.SUFFICIENT: "yellow",
            CompletionStatus.IN_PROGRESS: "blue",
            CompletionStatus.NEEDS_INPUT: "red"
        }
    
    def show_welcome(self):
        """Display welcome message and introduction."""
        welcome_text = """
        [bold blue]🚀 AI-Powered Startup Framework[/bold blue]
        [bold]Vision & Opportunity Playbook[/bold]
        
        This interactive tool will help you develop a comprehensive vision and 
        opportunity assessment for your startup idea. We'll guide you through 
        strategic questions and generate actionable insights.
        
        [dim]✨ Features:[/dim]
        • Smart question generation based on your responses
        • Real-time completion tracking
        • Parallel AI analysis for faster results
        • Professional documentation output
        
        [bold green]Let's build your vision together![/bold green]
        """
        
        panel = Panel(
            welcome_text,
            title="Welcome to the Vision & Opportunity Playbook",
            title_align="center",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
        self.console.print()
    
    def show_progress(self, workflow_state: WorkflowState):
        """Display current progress across all categories."""
        table = Table(title="Progress Overview", show_header=True, header_style="bold blue")
        table.add_column("Category", style="cyan", no_wrap=True)
        table.add_column("Progress", justify="center")
        table.add_column("Status", justify="center")
        
        for category, progress in workflow_state.completion_monitor.categories.items():
            # Create progress bar
            progress_bar = f"[{self.progress_colors[progress.status]}]"
            progress_bar += "█" * int(progress.progress * 20)
            progress_bar += "░" * (20 - int(progress.progress * 20))
            progress_bar += f"[/] {progress.progress:.0%}"
            
            # Status with emoji
            status_emoji = {
                CompletionStatus.COMPLETE: "✅",
                CompletionStatus.SUFFICIENT: "⚡",
                CompletionStatus.IN_PROGRESS: "🔄",
                CompletionStatus.NEEDS_INPUT: "❌"
            }
            
            status_text = f"{status_emoji[progress.status]} {progress.status.value}"
            
            table.add_row(
                category.value.replace("_", " ").title(),
                progress_bar,
                status_text
            )
        
        # Overall progress
        overall_progress = workflow_state.completion_monitor.overall_completion
        overall_bar = f"[bold green]{'█' * int(overall_progress * 30)}[/]"
        overall_bar += f"[dim]{'░' * (30 - int(overall_progress * 30))}[/]"
        overall_bar += f" {overall_progress:.0%}"
        
        table.add_row(
            "[bold]Overall Progress[/bold]",
            overall_bar,
            "✅ Ready" if workflow_state.completion_monitor.enough_info_reached else "🔄 In Progress"
        )
        
        self.console.print(table)
        self.console.print()
    
    def ask_question(self, question: Question, workflow_state: WorkflowState) -> Optional[str]:
        """Ask a question and get user response."""
        # Question panel
        question_panel = Panel(
            f"[bold]{question.question}[/bold]\n\n"
            f"[dim]Category: {question.category.value.replace('_', ' ').title()}[/dim]\n"
            f"[dim]Why this matters: {question.rationale}[/dim]",
            title=f"Question {workflow_state.questions_asked + 1}",
            border_style="yellow",
            padding=(1, 2)
        )
        
        self.console.print(question_panel)
        
        # Show completion status
        completion_text = f"Overall completion: {workflow_state.completion_monitor.overall_completion:.0%}"
        if workflow_state.completion_monitor.skip_available:
            completion_text += " • [yellow]Skip option available[/yellow]"
        
        self.console.print(f"[dim]{completion_text}[/dim]")
        self.console.print()
        
        # Get user response
        if question.skip_option:
            self.console.print("[dim]Options:[/dim]")
            self.console.print("• Type your answer")
            self.console.print("• Type 'skip' to skip remaining questions")
            self.console.print("• Type 'quit' to exit")
            self.console.print()
        
        response = Prompt.ask(
            "[bold green]Your answer[/bold green]",
            default="",
            show_default=False
        )
        
        if response.lower() == 'quit':
            return None
        elif response.lower() == 'skip':
            return 'skip'
        
        return response
    
    def show_task_execution(self, tasks: List[Task]) -> Dict[str, Any]:
        """Show task execution progress with live updates."""
        results = {}
        
        with Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.1f}%",
            TimeRemainingColumn(),
            console=self.console,
            transient=True
        ) as progress:
            
            task_progress = {}
            for task in tasks:
                task_progress[task.task_id] = progress.add_task(
                    f"[yellow]{task.name}[/yellow]",
                    total=task.estimated_time
                )
            
            # Simulate task execution
            for task in tasks:
                task.status = TaskStatus.IN_PROGRESS
                
                # Simulate work with progress updates
                for i in range(task.estimated_time):
                    progress.update(task_progress[task.task_id], advance=1)
                    time.sleep(0.1)  # Simulate work
                
                task.status = TaskStatus.COMPLETED
                # Mock result for demonstration
                results[task.task_id] = f"Completed: {task.name}"
        
        return results
    
    def show_vision_statement(self, vision_statement: VisionStatement):
        """Display generated vision statement variations."""
        self.console.print(Rule("[bold blue]Generated Vision Statements[/bold blue]"))
        
        for i, variation in enumerate(vision_statement.variations, 1):
            # Create variation panel
            variation_content = f"""
            [bold]{variation.statement}[/bold]
            
            [dim]Tone: {variation.tone.title()}[/dim]
            [dim]Emotional Appeal: {variation.emotional_appeal}/10[/dim]
            [dim]Clarity Score: {variation.clarity_score}/10[/dim]
            [dim]Differentiation: {variation.differentiation_score}/10[/dim]
            
            [italic]{variation.use_case}[/italic]
            """
            
            panel = Panel(
                variation_content,
                title=f"Vision Statement {i}",
                border_style="green" if variation.statement == vision_statement.recommended_choice else "blue",
                padding=(1, 2)
            )
            
            self.console.print(panel)
        
        # Show recommendation
        rec_panel = Panel(
            f"[bold green]Recommended Choice:[/bold green]\n\n"
            f"{vision_statement.recommended_choice}\n\n"
            f"[dim]Reasoning: {vision_statement.reasoning}[/dim]",
            title="💡 Recommendation",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(rec_panel)
        self.console.print()
    
    def show_tam_analysis(self, tam_result: TAMResult):
        """Display TAM analysis results."""
        self.console.print(Rule("[bold blue]Total Addressable Market Analysis[/bold blue]"))
        
        # Create TAM table
        table = Table(title="TAM Calculations", show_header=True, header_style="bold blue")
        table.add_column("Method", style="cyan", no_wrap=True)
        table.add_column("Market Size", justify="right")
        table.add_column("Addressable %", justify="right")
        table.add_column("TAM Estimate", justify="right")
        table.add_column("Confidence", justify="center")
        
        for method_name, calc in tam_result.calculations.items():
            table.add_row(
                method_name.replace("_", " ").title(),
                f"${calc.market_size:,.0f}",
                f"{calc.addressable_percentage:.1%}",
                f"${calc.tam_estimate:,.0f}",
                f"{calc.confidence_level:.0%}"
            )
        
        self.console.print(table)
        
        # Final range
        range_panel = Panel(
            f"[bold]Conservative:[/bold] ${tam_result.final_range.conservative:,.0f}\n"
            f"[bold]Recommended:[/bold] ${tam_result.final_range.recommended:,.0f}\n"
            f"[bold]Optimistic:[/bold] ${tam_result.final_range.optimistic:,.0f}",
            title="🎯 TAM Range",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(range_panel)
        self.console.print()
    
    def show_final_summary(self, workflow_state: WorkflowState):
        """Display final summary of the workflow."""
        self.console.print(Rule("[bold green]Vision & Opportunity Assessment Complete[/bold green]"))
        
        # Summary stats
        stats_table = Table(title="Session Summary", show_header=True, header_style="bold blue")
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", justify="right")
        
        stats_table.add_row("Questions Asked", str(workflow_state.questions_asked))
        stats_table.add_row("Completion Level", f"{workflow_state.completion_monitor.overall_completion:.0%}")
        stats_table.add_row("Components Generated", str(len(workflow_state.generated_components)))
        stats_table.add_row("Total Tokens Used", f"{workflow_state.cost_metrics.tokens_used:,}")
        stats_table.add_row("Processing Time", f"{workflow_state.cost_metrics.computation_time:.1f}s")
        
        self.console.print(stats_table)
        
        # Next steps
        next_steps = [
            "Review and refine your vision statement",
            "Validate TAM calculations with market research",
            "Develop detailed go-to-market strategy",
            "Create investor pitch deck",
            "Begin customer discovery interviews"
        ]
        
        next_steps_panel = Panel(
            "\n".join(f"• {step}" for step in next_steps),
            title="🎯 Recommended Next Steps",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(next_steps_panel)
        
        # Export options
        export_panel = Panel(
            "Your assessment has been saved to: [bold]vision_opportunity_assessment.md[/bold]\n\n"
            "This document contains all generated components and can be shared with:\n"
            "• Team members and co-founders\n"
            "• Advisors and mentors\n"
            "• Potential investors\n"
            "• Strategic partners",
            title="📄 Export & Sharing",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(export_panel)
        self.console.print()
    
    def show_error(self, error: str):
        """Display error message."""
        error_panel = Panel(
            f"[bold red]Error:[/bold red] {error}",
            title="❌ Error",
            border_style="red",
            padding=(1, 2)
        )
        
        self.console.print(error_panel)
        self.console.print()
    
    def show_status(self, message: str):
        """Display status message."""
        with Status(message, console=self.console) as status:
            time.sleep(1)  # Simulate processing
    
    def confirm_action(self, message: str) -> bool:
        """Ask for user confirmation."""
        return Confirm.ask(f"[yellow]{message}[/yellow]")
    
    def show_cost_warning(self, current_cost: Dict[str, Any], limits: Dict[str, Any]):
        """Display cost warning when approaching limits."""
        warning_text = "[bold yellow]⚠️ Cost Warning[/bold yellow]\n\n"
        
        for metric, current in current_cost.items():
            limit = limits.get(metric, 0)
            percentage = (current / limit) * 100 if limit > 0 else 0
            
            if percentage > 80:
                warning_text += f"• {metric}: {current}/{limit} ({percentage:.0f}%)\n"
        
        warning_panel = Panel(
            warning_text,
            title="Cost Monitor",
            border_style="yellow",
            padding=(1, 2)
        )
        
        self.console.print(warning_panel)
        self.console.print()
    
    def clear_screen(self):
        """Clear the console screen."""
        self.console.clear()
    
    def print_separator(self):
        """Print a visual separator."""
        self.console.print(Rule(style="dim"))
        self.console.print() 