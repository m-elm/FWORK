#!/usr/bin/env python3
"""
Main entry point for the Vision & Opportunity Playbook console application.
"""

import click
import sys
import os
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from workflow import VisionOpportunityWorkflow
from ui import VisionOpportunityUI


@click.command()
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.option('--config', default='.env', help='Path to configuration file')
@click.version_option(version='1.0.0', prog_name='Vision & Opportunity Playbook')
def main(debug, config):
    """
    AI-Powered Startup Framework - Vision & Opportunity Playbook
    
    An interactive console application that helps entrepreneurs develop
    comprehensive vision statements and opportunity assessments for their
    startup ideas.
    
    Features:
    - Smart question generation based on your responses
    - Real-time completion tracking  
    - Parallel AI analysis for faster results
    - Professional documentation output
    - Cost monitoring and optimization
    """
    
    # Load environment variables
    if os.path.exists(config):
        load_dotenv(config)
    
    # Initialize UI for error handling
    ui = VisionOpportunityUI()
    
    try:
        # Welcome message
        if debug:
            ui.console.print(f"[dim]Debug mode enabled[/dim]")
            ui.console.print(f"[dim]Config file: {config}[/dim]")
            ui.console.print()
        
        # Initialize and run workflow
        workflow = VisionOpportunityWorkflow()
        workflow.run()
        
    except KeyboardInterrupt:
        ui.console.print("\n[yellow]Goodbye! 👋[/yellow]")
        sys.exit(0)
    except Exception as e:
        if debug:
            ui.console.print_exception()
        else:
            ui.show_error(f"An unexpected error occurred: {str(e)}")
        sys.exit(1)


@click.group()
def cli():
    """Vision & Opportunity Playbook CLI tools."""
    pass


@cli.command()
@click.argument('assessment_file', type=click.Path(exists=True))
def validate(assessment_file):
    """Validate an existing assessment file."""
    ui = VisionOpportunityUI()
    
    try:
        with open(assessment_file, 'r') as f:
            content = f.read()
        
        # Basic validation
        required_sections = [
            "# Vision & Opportunity Assessment",
            "## Vision Statement",
            "## Total Addressable Market",
            "## Market Timing Analysis"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            ui.show_error(f"Missing sections: {', '.join(missing_sections)}")
        else:
            ui.console.print("[green]✅ Assessment file is valid![/green]")
            
    except Exception as e:
        ui.show_error(f"Failed to validate assessment: {str(e)}")


@cli.command()
@click.argument('assessment_file', type=click.Path(exists=True))
@click.option('--format', default='pdf', type=click.Choice(['pdf', 'html', 'docx']))
def export(assessment_file, format):
    """Export assessment to different formats."""
    ui = VisionOpportunityUI()
    
    try:
        if format == 'pdf':
            ui.show_error("PDF export not implemented yet")
        elif format == 'html':
            ui.show_error("HTML export not implemented yet")
        elif format == 'docx':
            ui.show_error("DOCX export not implemented yet")
        else:
            ui.show_error(f"Unsupported format: {format}")
            
    except Exception as e:
        ui.show_error(f"Failed to export assessment: {str(e)}")


@cli.command()
def demo():
    """Run a demo with sample data."""
    ui = VisionOpportunityUI()
    
    ui.console.print("[bold blue]🎮 Demo Mode[/bold blue]")
    ui.console.print()
    ui.console.print("This would run a demo with pre-filled responses...")
    ui.console.print("[dim]Demo mode not implemented yet[/dim]")


@cli.command()
def status():
    """Show application status and configuration."""
    ui = VisionOpportunityUI()
    
    from rich.table import Table
    
    table = Table(title="Application Status", show_header=True, header_style="bold blue")
    table.add_column("Component", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Details")
    
    # Check dependencies
    try:
        import rich
        table.add_row("Rich Library", "✅ OK", f"Version: {rich.__version__}")
    except ImportError:
        table.add_row("Rich Library", "❌ Missing", "Install with: pip install rich")
    
    try:
        import pydantic
        table.add_row("Pydantic", "✅ OK", f"Version: {pydantic.__version__}")
    except ImportError:
        table.add_row("Pydantic", "❌ Missing", "Install with: pip install pydantic")
    
    try:
        import jsonschema
        table.add_row("JSON Schema", "✅ OK", f"Version: {jsonschema.__version__}")
    except ImportError:
        table.add_row("JSON Schema", "❌ Missing", "Install with: pip install jsonschema")
    
    # Check configuration
    if os.path.exists('.env'):
        table.add_row("Configuration", "✅ OK", "Found .env file")
    else:
        table.add_row("Configuration", "⚠️ Warning", "No .env file found")
    
    # Check output directory
    if os.access('.', os.W_OK):
        table.add_row("Output Directory", "✅ OK", "Write permissions available")
    else:
        table.add_row("Output Directory", "❌ Error", "No write permissions")
    
    ui.console.print(table)


if __name__ == '__main__':
    # If called directly, run the main workflow
    if len(sys.argv) == 1:
        main()
    else:
        # Otherwise, use the CLI
        cli() 