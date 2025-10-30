#!/usr/bin/env python3
"""
Test script to demonstrate the difference between AI and mock modes.
"""

import os
import sys
from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import WorkflowState, UserResponse, QuestionCategory
from config import config
from ui import VisionOpportunityUI


def create_sample_workflow_state() -> WorkflowState:
    """Create a sample workflow state with your e-invoicing responses."""
    workflow_state = WorkflowState()
    
    # Add your actual responses
    responses = [
        ("developing e-invoicing app focusing on factur-x for french market first", QuestionCategory.PROBLEM_CLARITY),
        ("accountants and everyone working with e-invoices", QuestionCategory.PROBLEM_CLARITY),
        ("to allow companies be compliant with their invoices so they can share and receive the correct version of invoices", QuestionCategory.MARKET_CONTEXT),
        ("pdf to e-invoice feature", QuestionCategory.SOLUTION_UNIQUENESS),
        ("I don't know", QuestionCategory.SCALE_POTENTIAL),
        ("software engineer", QuestionCategory.EXECUTION_READINESS),
    ]
    
    for i, (response, category) in enumerate(responses, 1):
        workflow_state.add_response(f"q_{i}", response, category)
    
    return workflow_state


def test_mock_mode():
    """Test the mock mode."""
    print("🤖 Testing MOCK MODE...")
    
    # Import original agents
    from agents import QuestionGeneratorAgent, VisionStatementAgent, TAMCalculatorAgent
    
    workflow_state = create_sample_workflow_state()
    
    # Test question generation
    question_agent = QuestionGeneratorAgent()
    question = question_agent.generate_question(workflow_state)
    print(f"Mock Question: {question.question}")
    
    # Test vision statement
    vision_agent = VisionStatementAgent()
    vision = vision_agent.generate_vision_statement(workflow_state)
    print(f"Mock Vision: {vision.recommended_choice}")
    
    # Test TAM calculation
    tam_agent = TAMCalculatorAgent()
    tam = tam_agent.calculate_tam(workflow_state)
    print(f"Mock TAM: ${tam.final_range.recommended:,.0f}")
    
    return {
        "question": question.question,
        "vision": vision.recommended_choice,
        "tam": tam.final_range.recommended
    }


def test_smart_mode():
    """Test the smart mode."""
    print("\n🧠 Testing SMART MODE...")
    
    try:
        # Import smart agents
        from smart_agents import SmartQuestionGeneratorAgent, SmartVisionStatementAgent, SmartTAMCalculatorAgent
        
        workflow_state = create_sample_workflow_state()
        
        # Test question generation
        question_agent = SmartQuestionGeneratorAgent(use_ai=False)  # Use smart templates
        question = question_agent.generate_question(workflow_state)
        print(f"Smart Question: {question.question}")
        
        # Test vision statement
        vision_agent = SmartVisionStatementAgent(use_ai=False)  # Use smart templates
        vision = vision_agent.generate_vision_statement(workflow_state)
        print(f"Smart Vision: {vision.recommended_choice}")
        
        # Test TAM calculation
        tam_agent = SmartTAMCalculatorAgent(use_ai=False)  # Use smart estimation
        tam = tam_agent.calculate_tam(workflow_state)
        print(f"Smart TAM: ${tam.final_range.recommended:,.0f}")
        
        return {
            "question": question.question,
            "vision": vision.recommended_choice,
            "tam": tam.final_range.recommended
        }
    
    except ImportError as e:
        print(f"❌ Smart agents not available: {e}")
        return None


def test_ai_mode():
    """Test the AI mode."""
    print("\n🚀 Testing AI MODE...")
    
    if not config.ai_available:
        print("❌ AI mode not available - no OpenAI API key found")
        return None
    
    try:
        # Import smart agents with AI enabled
        from smart_agents import SmartQuestionGeneratorAgent, SmartVisionStatementAgent, SmartTAMCalculatorAgent
        
        workflow_state = create_sample_workflow_state()
        
        # Test question generation
        question_agent = SmartQuestionGeneratorAgent(use_ai=True)
        question = question_agent.generate_question(workflow_state)
        print(f"AI Question: {question.question}")
        
        # Test vision statement
        vision_agent = SmartVisionStatementAgent(use_ai=True)
        vision = vision_agent.generate_vision_statement(workflow_state)
        print(f"AI Vision: {vision.recommended_choice}")
        
        # Test TAM calculation
        tam_agent = SmartTAMCalculatorAgent(use_ai=True)
        tam = tam_agent.calculate_tam(workflow_state)
        print(f"AI TAM: ${tam.final_range.recommended:,.0f}")
        
        return {
            "question": question.question,
            "vision": vision.recommended_choice,
            "tam": tam.final_range.recommended
        }
    
    except Exception as e:
        print(f"❌ AI mode failed: {e}")
        return None


def main():
    """Main test function."""
    console = Console()
    ui = VisionOpportunityUI()
    
    # Show welcome
    welcome_panel = Panel(
        "[bold blue]🧪 AI vs Mock Mode Test[/bold blue]\n\n"
        "This script demonstrates the difference between:\n"
        "• [red]Mock Mode[/red] - Generic, template-based responses\n"
        "• [yellow]Smart Mode[/yellow] - Context-aware templates\n"
        "• [green]AI Mode[/green] - Real AI understanding\n\n"
        "[dim]Using your e-invoicing app responses as test data...[/dim]",
        title="Test Framework",
        border_style="blue"
    )
    console.print(welcome_panel)
    
    # Show configuration status
    config_panel = Panel(
        config.print_status(),
        title="Configuration Status",
        border_style="cyan"
    )
    console.print(config_panel)
    
    # Run tests
    mock_results = test_mock_mode()
    smart_results = test_smart_mode()
    ai_results = test_ai_mode()
    
    # Compare results
    console.print("\n" + "="*60)
    console.print("[bold]COMPARISON RESULTS[/bold]")
    console.print("="*60)
    
    table = Table(title="AI vs Mock Comparison", show_header=True, header_style="bold blue")
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Mock Mode", style="red")
    table.add_column("Smart Mode", style="yellow")
    table.add_column("AI Mode", style="green")
    
    # Questions
    table.add_row(
        "Next Question",
        mock_results.get("question", "N/A")[:50] + "..." if len(mock_results.get("question", "")) > 50 else mock_results.get("question", "N/A"),
        smart_results.get("question", "N/A")[:50] + "..." if smart_results and len(smart_results.get("question", "")) > 50 else smart_results.get("question", "N/A") if smart_results else "N/A",
        ai_results.get("question", "N/A")[:50] + "..." if ai_results and len(ai_results.get("question", "")) > 50 else ai_results.get("question", "N/A") if ai_results else "N/A"
    )
    
    # Vision statements
    table.add_row(
        "Vision Statement",
        mock_results.get("vision", "N/A")[:50] + "..." if len(mock_results.get("vision", "")) > 50 else mock_results.get("vision", "N/A"),
        smart_results.get("vision", "N/A")[:50] + "..." if smart_results and len(smart_results.get("vision", "")) > 50 else smart_results.get("vision", "N/A") if smart_results else "N/A",
        ai_results.get("vision", "N/A")[:50] + "..." if ai_results and len(ai_results.get("vision", "")) > 50 else ai_results.get("vision", "N/A") if ai_results else "N/A"
    )
    
    # TAM estimates
    table.add_row(
        "TAM Estimate",
        f"${mock_results.get('tam', 0):,.0f}",
        f"${smart_results.get('tam', 0):,.0f}" if smart_results else "N/A",
        f"${ai_results.get('tam', 0):,.0f}" if ai_results else "N/A"
    )
    
    console.print(table)
    
    # Show how to enable AI
    if not config.ai_available:
        howto_panel = Panel(
            "[bold yellow]🔧 How to Enable AI Mode[/bold yellow]\n\n"
            "1. Get an OpenAI API key from https://platform.openai.com/api-keys\n"
            "2. Copy sample.env to .env:\n"
            "   [dim]cp sample.env .env[/dim]\n"
            "3. Edit .env and add your API key:\n"
            "   [dim]OPENAI_API_KEY=your_actual_key_here[/dim]\n"
            "4. Run the app:\n"
            "   [dim]python main.py[/dim]\n\n"
            "[green]✅ AI mode will understand your e-invoicing concept![/green]",
            title="Setup Instructions",
            border_style="yellow"
        )
        console.print(howto_panel)
    
    console.print("\n[bold green]✅ Test completed![/bold green]")


if __name__ == "__main__":
    main() 