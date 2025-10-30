# Multi-Playbook Agent System - Complete Implementation Guide

## Overview

You now have a sophisticated **Multi-Playbook Agent System** that creates interconnected agents for your 15 startup playbooks. This guide explains exactly how it works and how to build it step by step.

## ✅ What You Already Have

Your existing foundation is excellent:
- **Smart Agents**: AI-powered agents with intelligent fallbacks
- **Workflow System**: Complete workflow orchestration
- **Data Models**: Comprehensive Pydantic models
- **UI System**: Rich console interface
- **Cost Tracking**: Built-in monitoring and limits

## 🎯 What We Built

### 1. Multi-Playbook Architecture
- **15 Interconnected Playbooks**: All playbooks from your framework
- **Central Coordinator**: Manages dependencies and information flow
- **Shared Knowledge Base**: Cross-playbook information sharing
- **Automatic Updates**: Changes in one playbook update others

### 2. Key Components Created

```
vision_opportunity/
├── multi_playbook_models.py      # Data models for multi-playbook system
├── playbook_coordinator.py       # Central orchestration system
├── playbook_agents.py            # Sample agents for different playbooks
├── multi_playbook_system.py      # Main user interface system
└── demo_multi_playbook.py        # Demo showing system in action
```

## 🚀 Quick Start

### Step 1: Run the Demo
```bash
cd vision_opportunity
python demo_multi_playbook.py
```

This shows how the system works with sample data.

### Step 2: Try the Interactive System
```bash
python multi_playbook_system.py
```

This starts the interactive interface where you can work on any playbook.

## 🔧 How to Extend the System

### Adding New Playbook Agents

To add a new agent for any of the remaining playbooks:

#### 1. Create the Agent Class

```python
# In playbook_agents.py

class UXDesignAgent(BasePlaybookAgent):
    """Agent for UX Design Playbook."""
    
    def __init__(self, use_ai: bool = True):
        super().__init__(
            PlaybookType.UX_DESIGN,
            "UXDesignAgent",
            {"max_tokens": 2000, "max_api_calls": 20}
        )
        self.use_ai = use_ai
    
    def generate_user_journey_maps(self, workflow_state):
        """Generate user journey maps based on product strategy."""
        # Implementation here
        pass
    
    def create_wireframes(self, user_stories):
        """Create wireframes based on user stories."""
        # Implementation here
        pass
    
    def _handle_update_message(self, message):
        """Handle updates from Product Strategy playbook."""
        if "product_details.features" in message.content.get("changes", {}):
            print("🔄 UX Design: Features updated, regenerating wireframes")
```

#### 2. Register the Agent

```python
# In playbook_agents.py, update PlaybookAgentFactory

@staticmethod
def create_agent(playbook_type: PlaybookType, use_ai: bool = True):
    if playbook_type == PlaybookType.UX_DESIGN:
        return UXDesignAgent(use_ai)
    # ... existing cases
```

#### 3. Add Dependencies

```python
# In playbook_coordinator.py, add to _initialize_dependencies()

PlaybookDependency(
    from_playbook=PlaybookType.PRODUCT_STRATEGY,
    to_playbook=PlaybookType.UX_DESIGN,
    dependency_type=DependencyType.REQUIRES,
    description="Product strategy defines UX requirements",
    trigger_fields=["user_stories", "feature_prioritization"],
    update_targets=["wireframes", "user_journey_maps"],
    priority=9
)
```

### Adding Custom Questions

Each agent can generate contextual questions based on shared knowledge:

```python
def generate_contextual_questions(self, workflow_state):
    """Generate questions based on what we already know."""
    
    questions = []
    
    # Base questions for this playbook
    base_questions = [
        "What is your main consideration for [PLAYBOOK_AREA]?",
        "How does this relate to your overall strategy?"
    ]
    
    # Adapt based on shared knowledge
    if self.shared_knowledge:
        if self.shared_knowledge.company_info.get('vision'):
            # We have vision, ask more specific questions
            vision = self.shared_knowledge.company_info['vision']
            base_questions.append(f"How does this align with your vision: {vision}?")
        
        if self.shared_knowledge.target_market.get('personas'):
            # We have customer data, focus on customer needs
            personas = self.shared_knowledge.target_market['personas']
            base_questions.append(f"How will this serve your {personas[0]['type']} customers?")
    
    # Convert to Question objects
    for q in base_questions:
        questions.append(Question(
            question=q,
            category=QuestionCategory.PROBLEM_CLARITY,
            rationale="Contextual question based on shared knowledge",
            completion_impact=0.2,
            skip_option=True,
            follow_up_hints=["Be specific", "Consider dependencies"]
        ))
    
    return questions
```

### Adding Cross-Playbook Intelligence

The system automatically shares information between playbooks:

```python
# When a playbook generates insights, it updates shared knowledge
def extract_insights(self, responses):
    insights = self.analyze_responses(responses)
    
    # Update shared knowledge
    if 'target_audience' in insights:
        self.coordinator.state.update_shared_knowledge(
            'target_market.audience', 
            insights['target_audience'], 
            self.playbook_type
        )
    
    # This automatically triggers updates to dependent playbooks
```

## 🔗 Understanding Dependencies

The system manages four types of dependencies:

### 1. REQUIRES (🔴)
```python
# Customer Discovery REQUIRES Vision & Opportunity
# Won't start until Vision is sufficient
PlaybookDependency(
    from_playbook=PlaybookType.VISION_OPPORTUNITY,
    to_playbook=PlaybookType.CUSTOMER_DISCOVERY,
    dependency_type=DependencyType.REQUIRES,
    # ...
)
```

### 2. INFLUENCES (🟡)
```python
# Vision INFLUENCES Customer Discovery
# Adjusts questions and approach
PlaybookDependency(
    from_playbook=PlaybookType.VISION_OPPORTUNITY,
    to_playbook=PlaybookType.CUSTOMER_DISCOVERY, 
    dependency_type=DependencyType.INFLUENCES,
    # ...
)
```

### 3. UPDATES (🔵)
```python
# Customer insights UPDATE Business Model
# One-way information flow
PlaybookDependency(
    from_playbook=PlaybookType.CUSTOMER_DISCOVERY,
    to_playbook=PlaybookType.BUSINESS_MODEL,
    dependency_type=DependencyType.UPDATES,
    # ...
)
```

### 4. SYNCS (🟢)
```python
# UX Design and Technical Development sync
# Bi-directional coordination
PlaybookDependency(
    from_playbook=PlaybookType.UX_DESIGN,
    to_playbook=PlaybookType.TECHNICAL_DEVELOPMENT,
    dependency_type=DependencyType.SYNCS,
    # ...
)
```

## 🎨 Customizing for Different Industries

The system adapts to different industries automatically:

```python
# In any agent, use shared knowledge to adapt
def adapt_to_industry(self):
    if self.shared_knowledge:
        company_info = self.shared_knowledge.company_info
        
        if 'fintech' in str(company_info).lower():
            # Fintech-specific logic
            return self.generate_fintech_questions()
        elif 'healthcare' in str(company_info).lower():
            # Healthcare-specific logic  
            return self.generate_healthcare_questions()
        else:
            # General business logic
            return self.generate_general_questions()
```

## 📊 Adding AI Integration

To add real AI capabilities to any agent:

```python
class SmartPlaybookAgent(BasePlaybookAgent):
    def __init__(self, playbook_type, use_ai=True):
        super().__init__(playbook_type, f"Smart{playbook_type.value}Agent", {...})
        
        if use_ai and os.getenv("OPENAI_API_KEY"):
            from ai_integration import AIIntegrationAgent
            self.ai_agent = AIIntegrationAgent()
            self.use_ai = True
        else:
            self.use_ai = False
    
    def generate_smart_content(self, context):
        if self.use_ai:
            try:
                return self.ai_agent.generate_content(context)
            except Exception as e:
                print(f"AI failed: {e}, using fallback")
        
        return self.generate_template_content(context)
```

## 🔧 Configuration and Deployment

### Environment Setup
```bash
# Required dependencies
pip install pydantic rich click python-dotenv

# Optional AI dependencies  
pip install openai  # For OpenAI integration
```

### Environment Variables
```bash
# .env file
OPENAI_API_KEY=your_key_here  # Optional for AI features
DEFAULT_MODEL=gpt-4o-mini     # AI model to use
MAX_TOKENS_PER_AGENT=2000     # Token limits
```

### Running in Production
```python
# For production deployment
system = MultiPlaybookSystem(use_ai=True)
system.coordinator.load_state("production_state.json")

# Process in batch mode
results = system.process_batch_questions(question_batch)
system.coordinator.save_state("production_state.json")
```

## 🎯 Implementation Priorities

### Phase 1: Core System (✅ Complete)
- Multi-playbook data models
- Central coordinator
- Basic agents for key playbooks
- Interactive system

### Phase 2: Enhanced Agents (Next)
1. **UX Design Agent**: Wireframes, user journeys
2. **Technical Development Agent**: Architecture, tech stack
3. **Financial Planning Agent**: Projections, funding
4. **Team & Culture Agent**: Hiring, culture design

### Phase 3: Advanced Features (Later)
1. **AI Integration**: Full OpenAI integration
2. **Export System**: PDF, Word, presentation exports
3. **Collaboration**: Multi-user support
4. **Analytics**: Progress analytics and insights

## 🚨 Common Issues and Solutions

### Issue: Agent Not Receiving Updates
```python
# Check dependency configuration
deps = coordinator.dependencies
relevant_deps = [d for d in deps if d.to_playbook == your_playbook_type]
print("Dependencies:", relevant_deps)

# Ensure agent is registered
agent = coordinator.playbook_agents.get(your_playbook_type)
if not agent:
    print("Agent not registered!")
```

### Issue: Shared Knowledge Not Updating
```python
# Check knowledge extraction
def _extract_shared_knowledge(self, playbook_type, artifacts):
    print(f"Extracting from {playbook_type}: {artifacts.keys()}")
    
    # Ensure proper key format
    self.state.update_shared_knowledge('company_info.key', value, playbook_type)
```

### Issue: Questions Not Contextual
```python
# Ensure shared knowledge is set
agent.set_shared_knowledge(coordinator.state.shared_knowledge)

# Check knowledge availability
if self.shared_knowledge:
    print("Available knowledge:", self.shared_knowledge.dict())
```

## 🎉 Success Metrics

Your system is working correctly when:

1. **✅ Dependencies Work**: Playbooks unlock as predecessors complete
2. **✅ Information Flows**: Changes in one playbook update others
3. **✅ Questions Adapt**: Questions become more specific as you provide information
4. **✅ Progress Tracks**: Overall progress increases as you complete playbooks
5. **✅ Artifacts Generate**: Each playbook produces useful outputs
6. **✅ State Persists**: You can resume sessions where you left off

## 🎯 Next Steps

1. **Run the demo** to see the system in action
2. **Try the interactive system** with your own startup idea
3. **Add agents** for the remaining playbooks you need most
4. **Customize dependencies** for your specific workflow
5. **Integrate AI** for more sophisticated responses
6. **Export results** to share with stakeholders

The system is designed to grow with your needs. Start with the core playbooks and expand as required! 