"""
Main Multi-Playbook System - Integration point for all interconnected startup playbooks.
This provides a simple interface for non-technical users to interact with the system.
"""

import os
import json
from typing import Dict, List, Optional, Any
from pathlib import Path

from playbook_coordinator import PlaybookCoordinator
from playbook_agents import PlaybookAgentFactory
from multi_playbook_models import PlaybookType, PlaybookStatus
from models import UserResponse, QuestionCategory
from ui import VisionOpportunityUI


class MultiPlaybookSystem:
    """Main system orchestrating all startup playbooks."""
    
    def __init__(self, use_ai: bool = True):
        self.coordinator = PlaybookCoordinator(use_ai)
        self.ui = VisionOpportunityUI()
        self.current_session_file = "current_session.json"
        
        # Initialize agents for key playbooks
        self._initialize_agents()
        
        # Load previous session if exists
        self._load_session()
    
    def _initialize_agents(self):
        """Initialize agents for all playbooks."""
        priority_playbooks = [
            PlaybookType.VISION_OPPORTUNITY,
            PlaybookType.CUSTOMER_DISCOVERY,
            PlaybookType.BUSINESS_MODEL,
            PlaybookType.PRODUCT_STRATEGY
        ]
        
        for playbook_type in priority_playbooks:
            agent = PlaybookAgentFactory.create_agent(playbook_type)
            agent.set_shared_knowledge(self.coordinator.state.shared_knowledge)
            self.coordinator.playbook_agents[playbook_type] = agent
    
    def start_interactive_session(self):
        """Start an interactive session with the user."""
        self.ui.console.print("[bold blue]🚀 Multi-Playbook Startup Framework[/bold blue]")
        self.ui.console.print("Welcome! This system will guide you through building comprehensive startup playbooks.")
        self.ui.console.print()
        
        while True:
            try:
                self._show_main_menu()
                choice = self._get_user_choice()
                
                if choice == "1":
                    self._work_on_playbook()
                elif choice == "2":
                    self._show_status_dashboard()
                elif choice == "3":
                    self._show_dependencies()
                elif choice == "4":
                    self._export_results()
                elif choice == "5":
                    self._save_and_exit()
                    break
                else:
                    self.ui.console.print("[red]Invalid choice. Please try again.[/red]")
                    
            except KeyboardInterrupt:
                self.ui.console.print("\n[yellow]Session saved. Goodbye! 👋[/yellow]")
                self._save_session()
                break
            except Exception as e:
                self.ui.show_error(f"An error occurred: {str(e)}")
    
    def _show_main_menu(self):
        """Display the main menu options."""
        self.ui.console.print("\n[bold]What would you like to do?[/bold]")
        self.ui.console.print("1. Work on a playbook")
        self.ui.console.print("2. View status dashboard")
        self.ui.console.print("3. View playbook dependencies")
        self.ui.console.print("4. Export results")
        self.ui.console.print("5. Save and exit")
        self.ui.console.print()
    
    def _get_user_choice(self) -> str:
        """Get user's menu choice."""
        return self.ui.console.input("[bold cyan]Your choice (1-5): [/bold cyan]").strip()
    
    def _work_on_playbook(self):
        """Let user work on a specific playbook."""
        # Get available playbooks
        available = self.coordinator.state.get_available_playbooks()
        
        if not available:
            self.ui.console.print("[yellow]No playbooks are currently available to work on.[/yellow]")
            self.ui.console.print("Some playbooks might be blocked by dependencies.")
            return
        
        # Show available playbooks
        self.ui.console.print("\n[bold]Available Playbooks:[/bold]")
        for i, playbook in enumerate(available, 1):
            state = self.coordinator.state.playbooks[playbook]
            status_color = {
                PlaybookStatus.NOT_STARTED: "white",
                PlaybookStatus.IN_PROGRESS: "yellow", 
                PlaybookStatus.SUFFICIENT: "green",
                PlaybookStatus.COMPLETE: "bright_green"
            }.get(state.status, "white")
            
            self.ui.console.print(f"{i}. [{status_color}]{playbook.value.replace('_', ' ').title()}[/{status_color}] "
                                f"(Progress: {state.progress:.0%}, Priority: {state.priority.value})")
        
        # Get recommendation
        recommended = self.coordinator.get_next_recommended_playbook()
        if recommended:
            rec_index = available.index(recommended) + 1
            self.ui.console.print(f"\n💡 [bold green]Recommended: Option {rec_index}[/bold green]")
        
        # Get user choice
        try:
            choice = int(self.ui.console.input("\nWhich playbook would you like to work on? ").strip())
            if 1 <= choice <= len(available):
                selected_playbook = available[choice - 1]
                self._run_playbook_session(selected_playbook)
            else:
                self.ui.console.print("[red]Invalid choice.[/red]")
        except ValueError:
            self.ui.console.print("[red]Please enter a valid number.[/red]")
    
    def _run_playbook_session(self, playbook_type: PlaybookType):
        """Run an interactive session for a specific playbook."""
        self.ui.console.print(f"\n[bold blue]Working on: {playbook_type.value.replace('_', ' ').title()}[/bold blue]")
        
        state = self.coordinator.state.playbooks[playbook_type]
        agent = self.coordinator.playbook_agents.get(playbook_type)
        
        if not agent:
            self.ui.console.print("[red]Agent not available for this playbook yet.[/red]")
            return
        
        # Process any pending messages for this agent
        agent.process_messages()
        
        # Generate contextual questions based on playbook type
        questions = self._generate_playbook_questions(playbook_type, state.workflow_state)
        
        if not questions:
            self.ui.console.print("[yellow]No questions available for this playbook at the moment.[/yellow]")
            return
        
        # Ask questions and collect responses
        responses_collected = 0
        for question in questions[:3]:  # Limit to 3 questions per session
            self.ui.console.print(f"\n[bold]{question.question}[/bold]")
            if question.follow_up_hints:
                self.ui.console.print(f"[dim]Hints: {', '.join(question.follow_up_hints)}[/dim]")
            
            response = self.ui.console.input("Your answer: ").strip()
            if response.lower() == 'skip':
                continue
                
            # Add response to workflow state
            state.workflow_state.add_response(
                question_id=f"{playbook_type.value}_{responses_collected}",
                response=response,
                category=question.category
            )
            responses_collected += 1
        
        # Update progress
        new_progress = min(state.progress + (responses_collected * 0.15), 1.0)
        
        # Generate artifacts if enough progress
        artifacts = {}
        if new_progress >= 0.5 and playbook_type in self.coordinator.playbook_agents:
            artifacts = self._generate_playbook_artifacts(playbook_type, state.workflow_state)
        
        # Update coordinator
        self.coordinator.update_playbook_progress(playbook_type, new_progress, artifacts)
        
        # Process any triggered updates
        self.coordinator.process_pending_updates()
        
        # Show progress
        self.ui.console.print(f"\n✅ Progress updated: {new_progress:.0%}")
        if artifacts:
            self.ui.console.print("🎯 Generated new artifacts based on your responses!")
    
    def _generate_playbook_questions(self, playbook_type: PlaybookType, workflow_state) -> List:
        """Generate questions for a specific playbook."""
        agent = self.coordinator.playbook_agents.get(playbook_type)
        if not agent:
            return []
        
        # Use existing question generation logic from agents
        if playbook_type == PlaybookType.CUSTOMER_DISCOVERY:
            return agent.generate_contextual_questions(workflow_state)
        elif playbook_type == PlaybookType.VISION_OPPORTUNITY:
            # Use existing Vision & Opportunity agent
            from smart_agents import SmartQuestionGeneratorAgent
            question_agent = SmartQuestionGeneratorAgent()
            return [question_agent.generate_question(workflow_state)]
        else:
            # Generic questions for other playbooks
            from models import Question
            return [Question(
                question=f"What are your main considerations for {playbook_type.value.replace('_', ' ')}?",
                category=QuestionCategory.PROBLEM_CLARITY,
                rationale="Gather general insights",
                completion_impact=0.2,
                skip_option=True,
                follow_up_hints=["Be specific", "Consider dependencies"]
            )]
    
    def _generate_playbook_artifacts(self, playbook_type: PlaybookType, workflow_state) -> Dict[str, Any]:
        """Generate artifacts for a specific playbook."""
        agent = self.coordinator.playbook_agents.get(playbook_type)
        if not agent:
            return {}
        
        artifacts = {}
        
        if playbook_type == PlaybookType.CUSTOMER_DISCOVERY:
            insights = agent.analyze_customer_responses(workflow_state.user_responses)
            artifacts.update(insights)
        
        elif playbook_type == PlaybookType.BUSINESS_MODEL:
            revenue_model = agent.generate_revenue_model_options(workflow_state)
            unit_economics = agent.calculate_unit_economics({})
            artifacts.update({
                "revenue_model": revenue_model,
                "unit_economics": unit_economics
            })
        
        elif playbook_type == PlaybookType.PRODUCT_STRATEGY:
            value_prop = agent.generate_value_proposition(workflow_state)
            features = agent.prioritize_features({})
            artifacts.update({
                "value_proposition": value_prop,
                "feature_prioritization": features
            })
        
        return artifacts
    
    def _show_status_dashboard(self):
        """Display comprehensive status dashboard."""
        from rich.table import Table
        from rich.progress import Progress, BarColumn, TextColumn
        
        status = self.coordinator.get_status_summary()
        
        # Overall progress
        with Progress(
            TextColumn("[bold blue]Overall Progress"),
            BarColumn(),
            TextColumn("{percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task("", completed=status["overall_progress"] * 100, total=100)
            self.ui.console.print()
        
        # Playbook status table
        table = Table(title="Playbook Status", show_header=True, header_style="bold blue")
        table.add_column("Playbook", style="cyan")
        table.add_column("Status", justify="center")
        table.add_column("Progress", justify="center") 
        table.add_column("Priority")
        table.add_column("Dependencies Met", justify="center")
        
        for playbook, details in status["playbook_statuses"].items():
            status_emoji = {
                "not_started": "⚪",
                "in_progress": "🟡",
                "sufficient": "🟢", 
                "complete": "✅"
            }.get(details["status"], "⚪")
            
            deps_emoji = "✅" if details["dependencies_met"] else "❌"
            
            table.add_row(
                playbook.replace('_', ' ').title(),
                f"{status_emoji} {details['status'].replace('_', ' ').title()}",
                f"{details['progress']:.0%}",
                details['priority'].replace('_', ' ').title(),
                deps_emoji
            )
        
        self.ui.console.print(table)
        
        # Show active insights
        if status["shared_knowledge_items"] > 0:
            self.ui.console.print(f"\n📊 [bold green]{status['shared_knowledge_items']} insights[/bold green] captured across playbooks")
        
        if status["pending_updates"] > 0:
            self.ui.console.print(f"🔄 [yellow]{status['pending_updates']} updates[/yellow] pending propagation")
    
    def _show_dependencies(self):
        """Show playbook dependencies in a visual format."""
        self.ui.console.print("\n[bold]Playbook Dependencies:[/bold]")
        
        for dep in self.coordinator.dependencies:
            color = {
                "requires": "red",
                "influences": "yellow", 
                "updates": "blue",
                "syncs": "green"
            }.get(dep.dependency_type.value, "white")
            
            self.ui.console.print(
                f"[{color}]{dep.from_playbook.value}[/{color}] "
                f"→ [{color}]{dep.dependency_type.value}[/{color}] → "
                f"[{color}]{dep.to_playbook.value}[/{color}]"
            )
            self.ui.console.print(f"   {dep.description}")
    
    def _export_results(self):
        """Export current results to files."""
        output_dir = Path("playbook_outputs")
        output_dir.mkdir(exist_ok=True)
        
        # Export overall status
        status = self.coordinator.get_status_summary()
        with open(output_dir / "overall_status.json", 'w') as f:
            json.dump(status, f, indent=2)
        
        # Export individual playbook artifacts
        for playbook_type, state in self.coordinator.state.playbooks.items():
            if state.generated_artifacts:
                filename = f"{playbook_type.value}_artifacts.json"
                with open(output_dir / filename, 'w') as f:
                    json.dump(state.generated_artifacts, f, indent=2, default=str)
        
        # Export shared knowledge
        shared_knowledge_dict = self.coordinator.state.shared_knowledge.dict()
        with open(output_dir / "shared_knowledge.json", 'w') as f:
            json.dump(shared_knowledge_dict, f, indent=2, default=str)
        
        self.ui.console.print(f"✅ Results exported to [bold]{output_dir.absolute()}[/bold]")
    
    def _save_session(self):
        """Save current session state."""
        self.coordinator.save_state(self.current_session_file)
    
    def _load_session(self):
        """Load previous session state."""
        self.coordinator.load_state(self.current_session_file)
    
    def _save_and_exit(self):
        """Save and exit the system."""
        self._save_session()
        self.ui.console.print("💾 Session saved successfully!")
        self.ui.console.print("👋 Thank you for using the Multi-Playbook Startup Framework!")


def main():
    """Main entry point for the multi-playbook system."""
    import sys
    
    # Check for AI availability
    use_ai = os.getenv("OPENAI_API_KEY") is not None
    if not use_ai:
        print("⚠️  No AI API key found. Running in template mode.")
        print("💡 Set OPENAI_API_KEY environment variable for AI-powered features.")
    
    try:
        system = MultiPlaybookSystem(use_ai=use_ai)
        system.start_interactive_session()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 