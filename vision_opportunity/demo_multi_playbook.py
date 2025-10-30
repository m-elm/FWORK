#!/usr/bin/env python3
"""
Demo script showing the Multi-Playbook System in action.
This demonstrates how the different playbooks interact and share information.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_playbook_system import MultiPlaybookSystem
from multi_playbook_models import PlaybookType
from playbook_coordinator import PlaybookCoordinator


def run_demo():
    """Run a demonstration of the multi-playbook system."""
    print("🎮 Multi-Playbook System Demo")
    print("=" * 50)
    
    # Initialize system
    system = MultiPlaybookSystem(use_ai=False)  # Use template mode for demo
    coordinator = system.coordinator
    
    print("✅ System initialized with 15 interconnected playbooks")
    print(f"📊 Overall progress: {coordinator.state.overall_progress:.0%}")
    print()
    
    # Simulate working on Vision & Opportunity
    print("🎯 Step 1: Working on Vision & Opportunity Playbook")
    print("-" * 40)
    
    vision_playbook = coordinator.state.playbooks[PlaybookType.VISION_OPPORTUNITY]
    
    # Simulate user responses
    sample_responses = [
        "We're building an e-invoicing solution for French businesses to comply with Factur-X regulations",
        "Our target market is French SMEs who struggle with invoice compliance",
        "The market opportunity is driven by mandatory e-invoicing coming in 2026",
        "We estimate a TAM of €2.5 billion for French e-invoicing market"
    ]
    
    for i, response in enumerate(sample_responses):
        vision_playbook.workflow_state.add_response(
            question_id=f"vision_demo_{i}",
            response=response,
            category=list(vision_playbook.workflow_state.completion_monitor.categories.keys())[i % 5]
        )
    
    # Update progress and generate artifacts
    vision_artifacts = {
        "vision_statement": {
            "recommended_choice": "We transform French businesses by eliminating invoice compliance challenges through automated e-invoicing to achieve regulatory compliance and efficiency",
            "variations": [
                {"statement": "We transform French businesses...", "tone": "ambitious"},
                {"statement": "We help French businesses...", "tone": "practical"}
            ]
        },
        "tam_calculation": {
            "final_range": {
                "conservative": 1750000000,
                "recommended": 2500000000, 
                "optimistic": 3250000000
            }
        }
    }
    
    coordinator.update_playbook_progress(PlaybookType.VISION_OPPORTUNITY, 0.8, vision_artifacts)
    print(f"✅ Vision & Opportunity: {coordinator.state.playbooks[PlaybookType.VISION_OPPORTUNITY].progress:.0%} complete")
    print("🎯 Generated: Vision statement and TAM calculation")
    
    # Process updates
    coordinator.process_pending_updates()
    print(f"🔄 Processed {len([u for u in coordinator.state.pending_updates if u.propagated])} cross-playbook updates")
    print()
    
    # Check what playbooks are now available
    available = coordinator.state.get_available_playbooks()
    print("📋 Available Playbooks After Vision & Opportunity:")
    for pb in available:
        deps_met = "✅" if coordinator.state.playbooks[pb].dependencies_met else "❌"
        print(f"   {deps_met} {pb.value.replace('_', ' ').title()}")
    print()
    
    # Simulate working on Customer Discovery
    print("👥 Step 2: Working on Customer Discovery Playbook")
    print("-" * 40)
    
    customer_playbook = coordinator.state.playbooks[PlaybookType.CUSTOMER_DISCOVERY]
    
    # Simulate customer discovery responses
    customer_responses = [
        "Our ideal customers are French SMEs with 10-500 employees who handle high invoice volumes",
        "They're currently struggling with manual invoice processing and compliance tracking",
        "Most are using basic accounting software that doesn't handle Factur-X properly",
        "They're willing to pay €100-300 per month for a complete compliance solution"
    ]
    
    for i, response in enumerate(customer_responses):
        customer_playbook.workflow_state.add_response(
            question_id=f"customer_demo_{i}",
            response=response,
            category=list(customer_playbook.workflow_state.completion_monitor.categories.keys())[i % 5]
        )
    
    customer_artifacts = {
        "customer_personas": [
            {
                "type": "B2B",
                "characteristics": ["SMEs 10-500 employees", "High invoice volume"],
                "needs": ["Compliance", "Efficiency", "Cost reduction"]
            }
        ],
        "pricing_insights": "€100-300 per month for compliance solution",
        "willingness_to_pay": "€100-300 monthly",
        "pain_points": ["Manual processing", "Compliance tracking", "Factur-X complexity"]
    }
    
    coordinator.update_playbook_progress(PlaybookType.CUSTOMER_DISCOVERY, 0.7, customer_artifacts)
    print(f"✅ Customer Discovery: {coordinator.state.playbooks[PlaybookType.CUSTOMER_DISCOVERY].progress:.0%} complete")
    print("👥 Generated: Customer personas and pricing insights")
    
    coordinator.process_pending_updates()
    print()
    
    # Simulate working on Business Model
    print("💰 Step 3: Working on Business Model Playbook")
    print("-" * 40)
    
    business_playbook = coordinator.state.playbooks[PlaybookType.BUSINESS_MODEL]
    
    business_artifacts = {
        "revenue_model": {
            "recommended": {
                "model": "subscription",
                "details": {
                    "description": "Monthly/annual recurring revenue",
                    "fit_score": 9  # High because of B2B customer persona
                }
            }
        },
        "unit_economics": {
            "customer_acquisition_cost": 150,
            "customer_lifetime_value": 2400,
            "ltv_cac_ratio": 16,
            "payback_period_months": 6,
            "health_indicators": {
                "ltv_cac_healthy": True,
                "payback_healthy": True,
                "margin_healthy": True
            }
        }
    }
    
    coordinator.update_playbook_progress(PlaybookType.BUSINESS_MODEL, 0.6, business_artifacts)
    print(f"✅ Business Model: {coordinator.state.playbooks[PlaybookType.BUSINESS_MODEL].progress:.0%} complete")
    print("💰 Generated: Subscription model with healthy unit economics (LTV/CAC: 16)")
    
    coordinator.process_pending_updates()
    print()
    
    # Show final status
    print("📊 Final System Status")
    print("=" * 30)
    
    status = coordinator.get_status_summary()
    print(f"Overall Progress: {status['overall_progress']:.1%}")
    print(f"Active Playbooks: {len(status['available_playbooks'])}")
    print(f"Shared Knowledge Items: {status['shared_knowledge_items']}")
    print()
    
    print("🔗 Cross-Playbook Connections Demonstrated:")
    print("• Vision & TAM → Customer Discovery (informed customer questions)")  
    print("• Customer personas → Business Model (influenced revenue model selection)")
    print("• Pricing insights → Business Model (updated unit economics)")
    print("• All insights stored in shared knowledge base")
    print()
    
    print("✨ Key Features Shown:")
    print("• ✅ Automatic dependency management")
    print("• ✅ Cross-playbook information sharing")
    print("• ✅ Smart recommendation engine")
    print("• ✅ Progress tracking and artifacts generation")
    print("• ✅ Persistent state management")
    
    return coordinator


def demonstrate_dependencies():
    """Show how dependencies work between playbooks."""
    print("\n🔗 Playbook Dependencies Visualization")
    print("=" * 40)
    
    coordinator = PlaybookCoordinator(use_ai=False)
    
    print("Key Dependency Flows:")
    
    dependency_flows = [
        ("Vision & Opportunity", "Customer Discovery", "Vision guides customer research"),
        ("Customer Discovery", "Product Strategy", "Customer insights define product requirements"),
        ("Product Strategy", "UX Design", "Product strategy defines user experience"),
        ("Business Model", "Financial Planning", "Revenue model drives financial projections"),
        ("UX Design + Tech Dev", "Project Execution", "Both influence development planning")
    ]
    
    for source, target, description in dependency_flows:
        print(f"📋 {source}")
        print(f"   ↓ {description}")
        print(f"📋 {target}")
        print()
    
    print("Dependency Types:")
    print("🔴 REQUIRES: Hard dependency (blocks until completed)")
    print("🟡 INFLUENCES: Soft dependency (adjusts behavior)")
    print("🔵 UPDATES: One-way information flow")
    print("🟢 SYNCS: Bi-directional synchronization")


if __name__ == "__main__":
    print("Multi-Playbook Startup Framework - Demo")
    print("This demonstrates interconnected agents working together")
    print()
    
    try:
        coordinator = run_demo()
        demonstrate_dependencies()
        
        print("\n🎯 Demo Complete!")
        print("To try the interactive system, run: python multi_playbook_system.py")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc() 