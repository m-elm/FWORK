"""
Sample playbook agents demonstrating how different playbooks integrate with the
central coordination system and handle cross-playbook dependencies.
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime

from agents import BaseAgent
from models import Question, QuestionCategory, WorkflowState, UserResponse, Citation
from multi_playbook_models import (
    PlaybookType, AgentCoordinationMessage, SharedKnowledge
)


class BasePlaybookAgent(BaseAgent):
    """Base class for all playbook-specific agents."""
    
    def __init__(self, playbook_type: PlaybookType, name: str, cost_limits: Dict[str, int]):
        super().__init__(name, cost_limits)
        self.playbook_type = playbook_type
        self.shared_knowledge: Optional[SharedKnowledge] = None
        self.incoming_messages: List[AgentCoordinationMessage] = []
        
    def set_shared_knowledge(self, shared_knowledge: SharedKnowledge):
        """Set reference to shared knowledge base."""
        self.shared_knowledge = shared_knowledge
    
    def receive_message(self, message: AgentCoordinationMessage):
        """Receive a coordination message from another agent."""
        self.incoming_messages.append(message)
    
    def process_messages(self):
        """Process pending coordination messages."""
        for message in self.incoming_messages:
            self._handle_message(message)
        self.incoming_messages.clear()
    
    def _handle_message(self, message: AgentCoordinationMessage):
        """Handle a specific coordination message."""
        if message.message_type == "update":
            self._handle_update_message(message)
        elif message.message_type == "request":
            self._handle_request_message(message)
    
    def _handle_update_message(self, message: AgentCoordinationMessage):
        """Handle update messages from other playbooks."""
        # Override in specific agents
        pass
    
    def _handle_request_message(self, message: AgentCoordinationMessage):
        """Handle request messages from other playbooks."""
        # Override in specific agents
        pass


class CustomerDiscoveryAgent(BasePlaybookAgent):
    """Agent for Customer Discovery & Validation Playbook."""
    
    def __init__(self, use_ai: bool = True):
        super().__init__(
            PlaybookType.CUSTOMER_DISCOVERY,
            "CustomerDiscoveryAgent",
            {"max_tokens": 2000, "max_api_calls": 25}
        )
        self.use_ai = use_ai
        
    def generate_contextual_questions(self, workflow_state: WorkflowState) -> List[Question]:
        """Generate customer discovery questions based on shared knowledge."""
        start_time = time.time()
        questions = []
        
        # Base questions
        base_questions = [
            "Who do you believe is your ideal customer?",
            "What problem are they trying to solve?",
            "How are they currently solving this problem?",
            "What would motivate them to try a new solution?",
            "How much would they be willing to pay for a solution?"
        ]
        
        # Adapt questions based on shared knowledge
        if self.shared_knowledge:
            target_market = self.shared_knowledge.target_market
            company_info = self.shared_knowledge.company_info
            
            # If we have TAM data, focus on validation
            if target_market.get('tam'):
                base_questions.extend([
                    f"Based on our TAM calculation of ${target_market['tam']['final_range']['recommended']:,.0f}, does this market size seem realistic?",
                    "What specific segment within this market should we focus on first?"
                ])
            
            # If we have vision statement, align customer discovery
            if company_info.get('vision'):
                vision = company_info['vision']['recommended_choice']
                base_questions.extend([
                    f"Given our vision '{vision}', which customers would most benefit from this?",
                    "What specific pain points does our vision address for them?"
                ])
        
        # Convert to Question objects
        for i, q in enumerate(base_questions[:5]):  # Limit to 5 questions
            questions.append(Question(
                question=q,
                category=QuestionCategory.PROBLEM_CLARITY,  # Map to existing categories
                rationale="Validates customer understanding and market assumptions",
                completion_impact=0.2,
                skip_option=False,
                follow_up_hints=["Be specific about customer segments", "Quantify pain points", "Describe current solutions"]
            ))
        
        self.track_cost(tokens=100, time_spent=time.time() - start_time)
        return questions
    
    def analyze_customer_responses(self, responses: List[UserResponse]) -> Dict[str, Any]:
        """Analyze customer discovery responses and extract insights."""
        start_time = time.time()
        
        insights = {
            "customer_personas": [],
            "pain_points": [],
            "willingness_to_pay": None,
            "current_solutions": [],
            "market_validation": "pending"
        }
        
        # Extract insights from responses
        all_text = " ".join([r.response.lower() for r in responses])
        
        # Simple keyword-based analysis (would use AI in production)
        if "businesses" in all_text or "companies" in all_text:
            insights["customer_personas"].append({
                "type": "B2B",
                "characteristics": ["Business customers", "Company decision makers"],
                "needs": ["Efficiency", "Cost reduction", "Compliance"]
            })
        
        if "consumers" in all_text or "individuals" in all_text:
            insights["customer_personas"].append({
                "type": "B2C", 
                "characteristics": ["Individual consumers", "Personal use"],
                "needs": ["Convenience", "Value", "Ease of use"]
            })
        
        # Extract pain points
        pain_keywords = ["problem", "issue", "challenge", "difficult", "expensive", "slow"]
        for response in responses:
            if any(keyword in response.response.lower() for keyword in pain_keywords):
                insights["pain_points"].append(response.response)
        
        # Look for pricing insights
        price_keywords = ["$", "cost", "price", "pay", "budget"]
        for response in responses:
            if any(keyword in response.response.lower() for keyword in price_keywords):
                insights["willingness_to_pay"] = response.response
        
        self.track_cost(tokens=150, time_spent=time.time() - start_time)
        return insights
    
    def _handle_update_message(self, message: AgentCoordinationMessage):
        """Handle updates from other playbooks."""
        if message.content.get("source") == "vision_opportunity":
            # Vision & Opportunity updated, adjust our customer discovery approach
            changes = message.content.get("changes", {})
            
            if "target_market.tam" in changes:
                # TAM was updated, we should validate with customers
                print(f"🔄 Customer Discovery: TAM updated to {changes['target_market.tam']}, adjusting validation questions")
            
            if "company_info.vision" in changes:
                # Vision statement updated, align customer research
                print(f"🔄 Customer Discovery: Vision updated, realigning customer research focus")


class BusinessModelAgent(BasePlaybookAgent):
    """Agent for Business Model Playbook."""
    
    def __init__(self, use_ai: bool = True):
        super().__init__(
            PlaybookType.BUSINESS_MODEL,
            "BusinessModelAgent", 
            {"max_tokens": 2500, "max_api_calls": 20}
        )
        self.use_ai = use_ai
    
    def generate_revenue_model_options(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Generate revenue model options based on customer discovery insights."""
        start_time = time.time()
        
        options = {
            "subscription": {
                "description": "Monthly/annual recurring revenue",
                "pros": ["Predictable revenue", "Customer retention", "Scalable"],
                "cons": ["Higher customer acquisition cost", "Churn risk"],
                "fit_score": 7
            },
            "transaction": {
                "description": "Fee per transaction or usage",
                "pros": ["Scales with usage", "Low barrier to entry"],
                "cons": ["Variable revenue", "Depends on transaction volume"],
                "fit_score": 6
            },
            "freemium": {
                "description": "Free basic version, paid premium features",
                "pros": ["Low acquisition cost", "Viral growth potential"],
                "cons": ["Low conversion rates", "High support costs"],
                "fit_score": 5
            }
        }
        
        # Adjust fit scores based on shared knowledge
        if self.shared_knowledge:
            customer_data = self.shared_knowledge.target_market
            if customer_data.get('personas'):
                personas = customer_data['personas']
                for persona in personas:
                    if persona.get('type') == 'B2B':
                        # B2B customers prefer subscription models
                        options['subscription']['fit_score'] += 2
                        options['transaction']['fit_score'] += 1
                    elif persona.get('type') == 'B2C':
                        # B2C customers prefer freemium/transaction
                        options['freemium']['fit_score'] += 2
                        options['transaction']['fit_score'] += 1
        
        # Select recommended model
        recommended = max(options.items(), key=lambda x: x[1]['fit_score'])
        
        result = {
            "options": options,
            "recommended": {
                "model": recommended[0],
                "details": recommended[1],
                "reasoning": f"Best fit based on customer type and market analysis (score: {recommended[1]['fit_score']})"
            }
        }
        
        self.track_cost(tokens=200, time_spent=time.time() - start_time)
        return result
    
    def calculate_unit_economics(self, pricing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate unit economics based on pricing insights."""
        start_time = time.time()
        
        # Default assumptions that would be refined with real data
        assumptions = {
            "customer_acquisition_cost": 100,
            "customer_lifetime_value": 500,
            "gross_margin": 0.8,
            "churn_rate": 0.05
        }
        
        # Adjust based on pricing insights from customer discovery
        if self.shared_knowledge and self.shared_knowledge.financial_data.get('pricing_insights'):
            pricing_insights = self.shared_knowledge.financial_data['pricing_insights']
            # Parse pricing insights and adjust assumptions
            # This would be more sophisticated in production
        
        unit_economics = {
            "customer_acquisition_cost": assumptions["customer_acquisition_cost"],
            "customer_lifetime_value": assumptions["customer_lifetime_value"],
            "ltv_cac_ratio": assumptions["customer_lifetime_value"] / assumptions["customer_acquisition_cost"],
            "payback_period_months": assumptions["customer_acquisition_cost"] / (assumptions["customer_lifetime_value"] * 12 * (1 - assumptions["churn_rate"])),
            "gross_margin_percent": assumptions["gross_margin"] * 100,
            "monthly_churn_rate": assumptions["churn_rate"] * 100
        }
        
        # Add health indicators
        unit_economics["health_indicators"] = {
            "ltv_cac_healthy": unit_economics["ltv_cac_ratio"] >= 3,
            "payback_healthy": unit_economics["payback_period_months"] <= 12,
            "margin_healthy": unit_economics["gross_margin_percent"] >= 70
        }
        
        self.track_cost(tokens=150, time_spent=time.time() - start_time)
        return unit_economics
    
    def _handle_update_message(self, message: AgentCoordinationMessage):
        """Handle updates from other playbooks."""
        changes = message.content.get("changes", {})
        
        if "target_market.personas" in changes:
            print("🔄 Business Model: Customer personas updated, recalculating revenue model fit")
        
        if "financial_data.pricing_insights" in changes:
            print("🔄 Business Model: Pricing insights updated, recalculating unit economics")


class ProductStrategyAgent(BasePlaybookAgent):
    """Agent for Product Strategy Playbook."""
    
    def __init__(self, use_ai: bool = True):
        super().__init__(
            PlaybookType.PRODUCT_STRATEGY,
            "ProductStrategyAgent",
            {"max_tokens": 3000, "max_api_calls": 25}
        )
        self.use_ai = use_ai
    
    def generate_value_proposition(self, workflow_state: WorkflowState) -> Dict[str, Any]:
        """Generate value proposition based on customer insights and business model."""
        start_time = time.time()
        
        value_prop = {
            "core_value": "We help customers solve their problems efficiently",
            "target_segment": "General business customers",
            "key_benefits": ["Efficiency", "Cost savings", "Ease of use"],
            "differentiation": "Unique approach to problem solving"
        }
        
        # Customize based on shared knowledge
        if self.shared_knowledge:
            # Use customer personas
            if self.shared_knowledge.target_market.get('personas'):
                personas = self.shared_knowledge.target_market['personas']
                if personas:
                    persona = personas[0]  # Use first persona
                    value_prop["target_segment"] = persona.get('type', 'General customers')
                    value_prop["key_benefits"] = persona.get('needs', ['Efficiency', 'Value'])
            
            # Use vision statement
            if self.shared_knowledge.company_info.get('vision'):
                vision = self.shared_knowledge.company_info['vision']['recommended_choice']
                value_prop["core_value"] = f"Aligned with vision: {vision}"
            
            # Use business model insights
            if self.shared_knowledge.financial_data.get('revenue_model'):
                revenue_model = self.shared_knowledge.financial_data['revenue_model']
                if revenue_model.get('recommended', {}).get('model') == 'subscription':
                    value_prop["key_benefits"].append("Ongoing value delivery")
        
        result = {
            "value_proposition": value_prop,
            "canvas": {
                "customer_jobs": ["Solve specific problems", "Improve efficiency"],
                "pain_relievers": ["Eliminates manual work", "Reduces costs"],
                "gain_creators": ["Increases productivity", "Provides insights"]
            }
        }
        
        self.track_cost(tokens=200, time_spent=time.time() - start_time)
        return result
    
    def prioritize_features(self, customer_insights: Dict[str, Any]) -> Dict[str, Any]:
        """Prioritize features based on customer pain points."""
        start_time = time.time()
        
        # Base feature set
        features = [
            {"name": "Core Problem Solver", "priority": "high", "effort": "medium", "impact": "high"},
            {"name": "User Dashboard", "priority": "medium", "effort": "low", "impact": "medium"},
            {"name": "Analytics & Reporting", "priority": "medium", "effort": "high", "impact": "medium"},
            {"name": "Mobile App", "priority": "low", "effort": "high", "impact": "low"},
            {"name": "API Integration", "priority": "low", "effort": "medium", "impact": "medium"}
        ]
        
        # Adjust priorities based on customer insights
        if self.shared_knowledge:
            personas = self.shared_knowledge.target_market.get('personas', [])
            for persona in personas:
                if persona.get('type') == 'B2B':
                    # B2B customers value integrations and analytics
                    for feature in features:
                        if feature['name'] in ['Analytics & Reporting', 'API Integration']:
                            feature['priority'] = 'high'
                elif persona.get('type') == 'B2C':
                    # B2C customers value mobile and simplicity
                    for feature in features:
                        if feature['name'] == 'Mobile App':
                            feature['priority'] = 'high'
        
        # Create roadmap
        roadmap = {
            "quarter_1": [f for f in features if f['priority'] == 'high'],
            "quarter_2": [f for f in features if f['priority'] == 'medium'],
            "quarter_3": [f for f in features if f['priority'] == 'low']
        }
        
        result = {
            "feature_list": features,
            "prioritization_framework": "Impact vs Effort Matrix",
            "roadmap": roadmap
        }
        
        self.track_cost(tokens=180, time_spent=time.time() - start_time)
        return result
    
    def _handle_update_message(self, message: AgentCoordinationMessage):
        """Handle updates from other playbooks."""
        changes = message.content.get("changes", {})
        
        if "target_market.personas" in changes:
            print("🔄 Product Strategy: Customer personas updated, reprioritizing features")
        
        if "financial_data.revenue_model" in changes:
            print("🔄 Product Strategy: Revenue model updated, adjusting value proposition")


class PlaybookAgentFactory:
    """Factory for creating playbook agents."""
    
    @staticmethod
    def create_agent(playbook_type: PlaybookType, use_ai: bool = True) -> BasePlaybookAgent:
        """Create an agent for the specified playbook type."""
        if playbook_type == PlaybookType.CUSTOMER_DISCOVERY:
            return CustomerDiscoveryAgent(use_ai)
        elif playbook_type == PlaybookType.BUSINESS_MODEL:
            return BusinessModelAgent(use_ai)
        elif playbook_type == PlaybookType.PRODUCT_STRATEGY:
            return ProductStrategyAgent(use_ai)
        # Add more agents as needed
        else:
            # Return a generic agent for unimplemented playbooks
            return BasePlaybookAgent(playbook_type, f"{playbook_type.value}_agent", {"max_tokens": 1000, "max_api_calls": 10}) 