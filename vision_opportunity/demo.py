#!/usr/bin/env python3
"""
Demo script showing how to enable AI and what the difference will be.
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import VisionOpportunityUI


def main():
    """Main demo function."""
    console = Console()
    ui = VisionOpportunityUI()
    
    # Title
    title = Text("🚀 AI-Powered Vision & Opportunity Playbook", style="bold blue")
    console.print(Columns([title], align="center"))
    console.print()
    
    # Show current status
    current_status = Panel(
        "[bold red]❌ CURRENT STATUS: MOCK MODE[/bold red]\n\n"
        "Your current output was generated using mock agents that:\n"
        "• Use static question templates\n"
        "• Generate generic vision statements\n"
        "• Don't understand your e-invoicing concept\n"
        "• Ignore specific details like 'Factur-X' and 'French market'\n\n"
        "[dim]Result: Generic output that doesn't reflect your business[/dim]",
        title="Current Implementation",
        border_style="red"
    )
    
    ai_status = Panel(
        "[bold green]✅ WITH AI MODE: INTELLIGENT UNDERSTANDING[/bold green]\n\n"
        "With AI integration, the system will:\n"
        "• Ask context-aware questions about e-invoicing\n"
        "• Understand Factur-X compliance requirements\n"
        "• Generate France-specific market analysis\n"
        "• Create relevant vision statements for fintech\n"
        "• Calculate TAM based on French B2B market\n\n"
        "[dim]Result: Personalized, relevant business insights[/dim]",
        title="AI-Powered Mode",
        border_style="green"
    )
    
    console.print(Columns([current_status, ai_status]))
    console.print()
    
    # Show the difference
    comparison_panel = Panel(
        "[bold]🔍 COMPARISON: Your E-Invoicing App[/bold]\n\n"
        "[red]Mock Mode Output:[/red]\n"
        '• Vision: "We solve complex challenges for businesses by innovative technology to transform their future"\n'
        '• Next Question: "What specific problem are you trying to solve?"\n'
        '• TAM: Generic $100M estimate\n\n'
        "[green]AI Mode Output (Expected):[/green]\n"
        '• Vision: "We streamline French business compliance through automated Factur-X e-invoicing to ensure seamless regulatory adherence"\n'
        '• Next Question: "What are the current Factur-X adoption rates in France, and what specific compliance challenges do your target businesses face?"\n'
        '• TAM: France-specific B2B invoicing market analysis\n\n'
        "[dim]The AI understands your specific business context![/dim]",
        title="Output Comparison",
        border_style="yellow"
    )
    
    console.print(comparison_panel)
    console.print()
    
    # Setup instructions
    setup_panel = Panel(
        "[bold blue]🔧 SETUP INSTRUCTIONS[/bold blue]\n\n"
        "[bold]Step 1: Get OpenAI API Key[/bold]\n"
        "• Go to https://platform.openai.com/api-keys\n"
        "• Create a new API key\n"
        "• Copy the key (starts with 'sk-')\n\n"
        "[bold]Step 2: Configure Environment[/bold]\n"
        "[dim]cp sample.env .env[/dim]\n"
        "[dim]# Edit .env and add your key:[/dim]\n"
        "[dim]OPENAI_API_KEY=sk-your-actual-key-here[/dim]\n\n"
        "[bold]Step 3: Run with AI[/bold]\n"
        "[dim]python main.py[/dim]\n\n"
        "[green]✅ The system will now understand your e-invoicing concept![/green]",
        title="Quick Setup",
        border_style="blue"
    )
    
    console.print(setup_panel)
    console.print()
    
    # Testing instructions
    test_panel = Panel(
        "[bold yellow]🧪 TESTING THE DIFFERENCE[/bold yellow]\n\n"
        "Run this command to see the comparison:\n"
        "[dim]python test_ai.py[/dim]\n\n"
        "This will show you:\n"
        "• Mock mode (current generic output)\n"
        "• Smart mode (context-aware templates)\n"
        "• AI mode (real AI understanding)\n\n"
        "[dim]Perfect for testing before full setup![/dim]",
        title="Test Before Setup",
        border_style="yellow"
    )
    
    console.print(test_panel)
    console.print()
    
    # Benefits panel
    benefits_panel = Panel(
        "[bold green]🎯 BENEFITS OF AI MODE[/bold green]\n\n"
        "For your e-invoicing app specifically:\n"
        "• Questions about French regulatory requirements\n"
        "• Vision statements mentioning Factur-X compliance\n"
        "• TAM calculations for French B2B market\n"
        "• Market timing analysis for EU e-invoicing mandates\n"
        "• Exit strategy considering regulatory landscape\n\n"
        "[bold]Result: Professional, investor-ready assessment[/bold]",
        title="AI Benefits",
        border_style="green"
    )
    
    console.print(benefits_panel)
    console.print()
    
    # Cost information
    cost_panel = Panel(
        "[bold cyan]💰 COST INFORMATION[/bold cyan]\n\n"
        "OpenAI API costs for a full assessment:\n"
        "• Typical usage: 3,000-5,000 tokens\n"
        "• GPT-4 cost: ~$0.15-0.25 per assessment\n"
        "• One-time setup, huge value improvement\n\n"
        "[dim]Much cheaper than hiring a consultant![/dim]",
        title="Cost Breakdown",
        border_style="cyan"
    )
    
    console.print(cost_panel)
    console.print()
    
    # Final call to action
    cta_panel = Panel(
        "[bold blue]🚀 READY TO UPGRADE?[/bold blue]\n\n"
        "[bold]Current state:[/bold] Generic, template-based output\n"
        "[bold]With AI:[/bold] Intelligent, context-aware insights\n\n"
        "[green]Your e-invoicing app deserves better than generic templates![/green]\n\n"
        "[bold]Next steps:[/bold]\n"
        "1. [dim]python test_ai.py[/dim] - See the difference\n"
        "2. Get OpenAI API key\n"
        "3. [dim]cp sample.env .env[/dim] - Configure\n"
        "4. [dim]python main.py[/dim] - Run with AI\n\n"
        "[bold yellow]Transform your startup assessment today! 🎯[/bold yellow]",
        title="Ready to Transform?",
        border_style="blue"
    )
    
    console.print(cta_panel)


if __name__ == "__main__":
    main() 