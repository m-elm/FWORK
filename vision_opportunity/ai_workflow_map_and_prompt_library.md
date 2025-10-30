# AI Workflow Map & Prompt Library: Vision & Opportunity Playbook

## 1. AI Workflow Architecture

### Overall Flow
```
User Input → Smart Information Gathering → Parallel Multi-Agent Processing → Validation & Refinement → Output Generation → Documentation
```

### Detailed Workflow Map

#### Phase 1: Smart Information Gathering (Interactive Questioning)
**Input:** User responses to guided questions  
**AI Tools:** Conversational Agent + Dynamic Question Generator + Completion Monitor  
**Output:** Structured data collection with completion tracking  
**Quality Gate:** 80% completion threshold OR user "Skip for now"

#### Phase 2: Market Intelligence (RAG + DeepSearch)
**Input:** Industry keywords, problem statements  
**AI Tools:** Two-pass RAG system + DeepSearch + Embedding similarity + Cross-encoder reranking  
**Output:** Market context, trends, competitive landscape with citations

#### Phase 3: Analysis & Synthesis (Parallel Multi-Agent System)
**Input:** Collected data + market intelligence  
**AI Tools:** Orchestrated parallel/serial agents with cost monitoring  
**Output:** Analyzed insights for each playbook component with confidence scores

#### Phase 4: Generation & Validation (LLM + Human-in-the-Loop)
**Input:** Synthesized insights  
**AI Tools:** Content generation LLM + JSON schema validation + citation tracking  
**Output:** Draft components with confidence scores and quality metrics

#### Phase 5: Documentation & Integration
**Input:** Validated components  
**AI Tools:** Documentation generator + template engine + cost tracker  
**Output:** Formatted deliverables with metadata

## 2. Modular Prompt Library

### 2.1 Smart Information Gathering Prompts

#### Completion Monitor System
```
COMPLETION_MONITOR_SCHEMA = {
    "type": "object",
    "properties": {
        "categories": {
            "type": "object",
            "properties": {
                "problem_clarity": {"type": "number", "minimum": 0, "maximum": 1},
                "market_context": {"type": "number", "minimum": 0, "maximum": 1},
                "solution_uniqueness": {"type": "number", "minimum": 0, "maximum": 1},
                "scale_potential": {"type": "number", "minimum": 0, "maximum": 1},
                "execution_readiness": {"type": "number", "minimum": 0, "maximum": 1}
            },
            "required": ["problem_clarity", "market_context", "solution_uniqueness", "scale_potential", "execution_readiness"]
        },
        "overall_completion": {"type": "number", "minimum": 0, "maximum": 1},
        "enough_info_reached": {"type": "boolean"},
        "missing_critical_info": {"type": "array", "items": {"type": "string"}},
        "skip_available": {"type": "boolean"}
    },
    "required": ["categories", "overall_completion", "enough_info_reached", "missing_critical_info", "skip_available"]
}

SYSTEM_PROMPT_COMPLETION_MONITOR = """
Monitor information gathering completeness using JSON schema validation.

CURRENT_DATA: {collected_data}
COMPLETION_THRESHOLD: 0.8

Evaluate completeness for each category:
- problem_clarity: Problem statement, pain points, target audience
- market_context: Industry, timing, competitive landscape  
- solution_uniqueness: Value proposition, differentiation
- scale_potential: Market size indicators, growth potential
- execution_readiness: Founder background, resources

Return JSON matching COMPLETION_MONITOR_SCHEMA.

RULES:
- If overall_completion ≥ 0.8 OR user requested skip → enough_info_reached = true
- missing_critical_info should be specific (e.g., "Missing target customer ARPU estimate")
- skip_available = true when user feels interrogated (>8 questions asked)
"""
```

#### Question Generator
```
SYSTEM_PROMPT_QUESTION_GENERATOR = """
Generate the next most valuable question with completion awareness:

COMPLETION_STATUS: {completion_status}
CURRENT_GAPS: {missing_critical_info}
QUESTION_COUNT: {questions_asked}
USER_SENTIMENT: {user_engagement_score}

QUESTION_STRATEGY:
- If completion ≥ 80%: Offer to proceed or refine
- If question_count > 8: Suggest skip option
- If user_engagement_score < 0.6: Simplify and focus
- Prioritize gaps that unlock multiple components

OUTPUT_SCHEMA:
{
  "question": "Your specific question here",
  "category": "PROBLEM_CLARITY",
  "rationale": "Why this question matters now",
  "completion_impact": 0.15,
  "skip_option": true,
  "follow_up_hints": ["potential", "follow", "ups"]
}

Always provide skip option after 6+ questions with explanation of current completeness.
"""
```

### 2.2 Component-Specific Prompts

#### Vision Statement Generator with Schema Validation
```
VISION_STATEMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "variations": {
            "type": "array",
            "items": {
                "type": "object", 
                "properties": {
                    "statement": {"type": "string", "minLength": 10, "maxLength": 200},
                    "tone": {"type": "string", "enum": ["ambitious", "practical", "disruptive"]},
                    "emotional_appeal": {"type": "number", "minimum": 1, "maximum": 10},
                    "clarity_score": {"type": "number", "minimum": 1, "maximum": 10},
                    "differentiation_score": {"type": "number", "minimum": 1, "maximum": 10},
                    "use_case": {"type": "string"}
                },
                "required": ["statement", "tone", "emotional_appeal", "clarity_score", "differentiation_score", "use_case"]
            },
            "minItems": 3,
            "maxItems": 3
        },
        "recommended_choice": {"type": "string"},
        "reasoning": {"type": "string"},
        "citations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "date_retrieved": {"type": "string", "format": "date"},
                    "relevance_score": {"type": "number", "minimum": 0, "maximum": 1},
                    "content_snippet": {"type": "string"}
                },
                "required": ["source", "date_retrieved", "relevance_score"]
            }
        }
    },
    "required": ["variations", "recommended_choice", "reasoning", "citations"]
}

SYSTEM_PROMPT_VISION_STATEMENT = """
Create compelling vision statements with JSON schema validation.

FRAMEWORK: "We [ACTION] for [TARGET_AUDIENCE] by [UNIQUE_APPROACH] to [ULTIMATE_OUTCOME]"

INPUT_DATA: {input_data}
MARKET_CONTEXT: {market_intelligence}
COST_BUDGET: {max_tokens}

Generate response matching VISION_STATEMENT_SCHEMA.

COST_MONITORING:
- Track token usage internally
- Limit chain-of-thought to essential reasoning
- Cap at {max_tokens} tokens total

CITATION_REQUIREMENTS:
- Include date_retrieved for freshness tracking
- Minimum relevance_score of 0.6
- Maximum 5 citations per component
"""
```

#### Problem/Mission Brief Generator
```
SYSTEM_PROMPT_PROBLEM_BRIEF = """
Create a comprehensive Problem/Mission Brief using this structure:

INPUTS:
- Core problem: {core_problem}
- Target personas: {target_personas}
- Current solutions: {current_solutions}
- Pain points: {pain_points}
- Market context: {market_context}

OUTPUT_STRUCTURE:
1. PROBLEM STATEMENT (2-3 sentences)
   - What specific problem exists?
   - Who experiences this problem?
   - Why is it painful/costly?

2. MISSION STATEMENT (1-2 sentences)
   - Our purpose in solving this problem
   - The change we want to create

3. PROBLEM VALIDATION (bullet points)
   - Evidence that this problem matters
   - Quantified impact where possible
   - Trends making it more urgent

4. SOLUTION IMPERATIVE (1 sentence)
   - Why this problem needs solving now

Use data from: {market_research_data}
Reference competitors: {competitor_analysis}
"""
```

#### Market Timing Analysis Generator
```
SYSTEM_PROMPT_TIMING_ANALYSIS = """
Analyze market timing using the TIMING framework:

T - Technology enablers and barriers
I - Industry trends and shifts  
M - Market maturity and readiness
I - Infrastructure and ecosystem
N - Narrative and cultural momentum
G - Gaps in current solutions

INPUTS:
- Industry: {industry}
- Technology stack: {technology}
- Market research: {market_data}
- Competitive landscape: {competitors}
- Regulatory environment: {regulations}

ANALYSIS PROCESS:
1. Score each TIMING factor (1-10)
2. Identify 3 key timing advantages
3. Highlight 2 potential timing risks
4. Recommend optimal entry window
5. Suggest timing-based strategies

OUTPUT FORMAT:
- Executive summary (2 sentences)
- Timing score breakdown
- Key opportunities table
- Risk mitigation strategies
- Recommended timeline
"""
```

#### TAM Calculator with Cost Monitoring
```
TAM_CALCULATOR_SCHEMA = {
    "type": "object",
    "properties": {
        "calculations": {
            "type": "object",
            "properties": {
                "top_down": {
                    "type": "object",
                    "properties": {
                        "market_size": {"type": "number"},
                        "addressable_percentage": {"type": "number"},
                        "tam_estimate": {"type": "number"},
                        "confidence_level": {"type": "number", "minimum": 0, "maximum": 1},
                        "assumptions": {"type": "array", "items": {"type": "string"}},
                        "calculation_steps": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["market_size", "addressable_percentage", "tam_estimate", "confidence_level", "assumptions"]
                },
                "bottom_up": {
                    "type": "object",
                    "properties": {
                        "target_customers": {"type": "number"},
                        "arpu": {"type": "number"},
                        "tam_estimate": {"type": "number"},
                        "confidence_level": {"type": "number", "minimum": 0, "maximum": 1},
                        "assumptions": {"type": "array", "items": {"type": "string"}},
                        "calculation_steps": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["target_customers", "arpu", "tam_estimate", "confidence_level", "assumptions"]
                }
            },
            "required": ["top_down", "bottom_up"]
        },
        "final_range": {
            "type": "object",
            "properties": {
                "conservative": {"type": "number"},
                "optimistic": {"type": "number"},
                "recommended": {"type": "number"}
            },
            "required": ["conservative", "optimistic", "recommended"]
        },
        "validation_checks": {"type": "array", "items": {"type": "string"}},
        "citations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "date_retrieved": {"type": "string", "format": "date"},
                    "relevance_score": {"type": "number", "minimum": 0, "maximum": 1},
                    "data_point": {"type": "string"}
                },
                "required": ["source", "date_retrieved", "relevance_score", "data_point"]
            }
        },
        "cost_metrics": {
            "type": "object",
            "properties": {
                "tokens_used": {"type": "number"},
                "computation_time": {"type": "number"},
                "api_calls": {"type": "number"}
            },
            "required": ["tokens_used", "computation_time", "api_calls"]
        }
    },
    "required": ["calculations", "final_range", "validation_checks", "citations", "cost_metrics"]
}

SYSTEM_PROMPT_TAM_CALCULATOR = """
Calculate TAM with cost monitoring and schema validation.

INPUTS: {inputs}
MARKET_DATA: {market_intelligence}
TOKEN_LIMIT: {max_tokens}

Return JSON matching TAM_CALCULATOR_SCHEMA.

COST_MONITORING_RULES:
- Track all token usage in cost_metrics
- Limit detailed calculations to essential steps
- Cap chain-of-thought reasoning at 500 tokens
- Alert if approaching token limit

CITATION_REQUIREMENTS:
- All data sources must include date_retrieved
- Flag sources older than 12 months
- Minimum relevance_score of 0.6
- Include specific data_point referenced
"""
```

#### Exit Strategy Generator
```
SYSTEM_PROMPT_EXIT_STRATEGY = """
Develop exit strategy considerations based on:

BUSINESS_CONTEXT:
- Industry: {industry}
- Business model: {business_model}
- Market position: {market_position}
- Revenue model: {revenue_model}
- Competitive advantages: {advantages}

ANALYSIS_FRAMEWORK:
1. ACQUISITION_TARGETS
   - Strategic acquirers in industry
   - Financial acquirers (PE/VC)
   - Acquisition rationale and timing

2. IPO_POTENTIAL
   - Market cap requirements
   - Growth trajectory needed
   - Comparable public companies

3. STRATEGIC_PARTNERSHIPS
   - Joint venture opportunities
   - Licensing potential
   - Distribution partnerships

OUTPUT_STRUCTURE:
- Primary exit scenario (with rationale)
- Secondary exit options
- Value creation milestones
- Timeline considerations
- Strategic implications for current decisions
"""
```

### 2.3 Orchestration Prompts

#### Workflow Coordinator
```
WORKFLOW_COORDINATOR_SCHEMA = {
    "type": "object",
    "properties": {
        "next_action": {"type": "string", "enum": ["ASK_QUESTION", "PARALLEL_STEP", "SERIAL_STEP", "VALIDATE", "COMPLETE"]},
        "parallel_tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "agent": {"type": "string"},
                    "estimated_time": {"type": "number"},
                    "dependencies": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["task", "agent", "estimated_time"]
            }
        },
        "serial_tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "task": {"type": "string"},
                    "agent": {"type": "string"},
                    "prerequisites": {"type": "array", "items": {"type": "string"}},
                    "estimated_time": {"type": "number"}
                },
                "required": ["task", "agent", "prerequisites", "estimated_time"]
            }
        },
        "quality_issues": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "issue": {"type": "string"},
                    "severity": {"type": "string", "enum": ["low", "medium", "high"]},
                    "component": {"type": "string"},
                    "suggestion": {"type": "string"}
                },
                "required": ["issue", "severity", "component", "suggestion"]
            }
        },
        "completion_estimate": {"type": "number"},
        "cost_projection": {"type": "number"}
    },
    "required": ["next_action", "completion_estimate", "cost_projection"]
}

SYSTEM_PROMPT_COORDINATOR = """
Coordinate workflow with parallel/serial task optimization.

CURRENT_STATE: {current_state}
COMPLETION_STATUS: {completion_status}
AVAILABLE_AGENTS: {agent_pool}
COST_BUDGET: {remaining_budget}

Return JSON matching WORKFLOW_COORDINATOR_SCHEMA.

PARALLEL_TASK_RULES:
- TAM calculation and timing analysis can run in parallel
- Vision statement and problem brief can run in parallel
- Exit strategy requires TAM completion (serial dependency)

SERIAL_TASK_RULES:
- Market intelligence must complete before TAM calculation
- Problem brief must complete before exit strategy
- All components must complete before final validation

QUALITY_ISSUE_SPECIFICITY:
Instead of "input_quality_score is low", specify:
- "Missing target customer ARPU estimate"
- "Industry classification needs refinement"
- "Competitive positioning unclear"

COST_OPTIMIZATION:
- Prioritize high-impact, low-cost tasks
- Bundle similar API calls
- Use cached results when possible
"""
```

#### Quality Assurance Prompt
```
QUALITY_ASSURANCE_SCHEMA = {
    "type": "object",
    "properties": {
        "component_scores": {
            "type": "object",
            "properties": {
                "vision_statement": {
                    "type": "object",
                    "properties": {
                        "clarity": {"type": "number", "minimum": 1, "maximum": 10},
                        "completeness": {"type": "number", "minimum": 1, "maximum": 10},
                        "consistency": {"type": "number", "minimum": 1, "maximum": 10},
                        "credibility": {"type": "number", "minimum": 1, "maximum": 10},
                        "compelling": {"type": "number", "minimum": 1, "maximum": 10},
                        "specific_issues": {"type": "array", "items": {"type": "string"}},
                        "improvement_suggestions": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["clarity", "completeness", "consistency", "credibility", "compelling"]
                }
            }
        },
        "overall_quality": {"type": "number", "minimum": 1, "maximum": 10},
        "approval_status": {"type": "string", "enum": ["approved", "needs_revision", "rejected"]},
        "priority_improvements": {"type": "array", "items": {"type": "string"}},
        "citations_health": {
            "type": "object",
            "properties": {
                "total_citations": {"type": "number"},
                "fresh_citations": {"type": "number"},
                "stale_citations": {"type": "number"},
                "outdated_citations": {"type": "number"}
            },
            "required": ["total_citations", "fresh_citations", "stale_citations", "outdated_citations"]
        }
    },
    "required": ["component_scores", "overall_quality", "approval_status", "citations_health"]
}

SYSTEM_PROMPT_QA = """
Evaluate deliverables with universal JSON schema validation.

DELIVERABLES: {deliverables}
CITATION_FRESHNESS_THRESHOLD: 90 days

Return JSON matching QUALITY_ASSURANCE_SCHEMA.

QUALITY_EVALUATION_RULES:
- Clarity: Easy to understand and actionable
- Completeness: All required components present
- Consistency: Aligned across all elements
- Credibility: Backed by data and logic
- Compelling: Inspires action and investment

CITATION_HEALTH_CHECK:
- Fresh: Retrieved within 90 days
- Stale: 90-365 days old
- Outdated: >365 days old
- Auto-flag outdated citations for refresh

SPECIFIC_ISSUE_EXAMPLES:
- "Vision statement lacks quantifiable outcome"
- "TAM calculation missing bottom-up validation"
- "Exit strategy relies on outdated market data"
- "Problem brief needs stronger pain point evidence"
"""
```

### 2.4 RAG and DeepSearch Integration

#### Two-Pass RAG System
```
RAG_CONFIG = {
    "recall_pass": {
        "similarity_threshold": 0.6,
        "max_results": 50,
        "embedding_model": "text-embedding-3-large",
        "search_strategy": "cast_wide_net"
    },
    "rerank_pass": {
        "model": "cross-encoder/ms-marco-MiniLM-L-12-v2",
        "top_k": 10,
        "relevance_threshold": 0.8,
        "context_window": 4000
    },
    "citation_tracking": {
        "include_date_retrieved": True,
        "freshness_threshold_days": 90,
        "auto_flag_stale": True,
        "min_relevance_score": 0.6
    }
}

SYSTEM_PROMPT_RAG = """
Execute two-pass RAG with citation tracking.

QUERY: {search_query}
DOMAIN: {search_domain}
RECALL_THRESHOLD: 0.6
RERANK_THRESHOLD: 0.8

RECALL_PASS:
- Cast wide net with similarity ≥ 0.6
- Gather up to 50 potential sources
- Include diverse perspectives

RERANK_PASS:
- Use cross-encoder for precise relevance scoring
- Keep only top 10 most relevant sources
- Ensure relevance ≥ 0.8

CITATION_REQUIREMENTS:
- date_retrieved for all sources
- Flag sources older than 90 days
- Include relevance_score in metadata
- Provide content_snippet for context

OUTPUT_SCHEMA:
{
  "sources": [
    {
      "content": "extracted text",
      "source": "source identifier",
      "date_retrieved": "2024-01-15",
      "relevance_score": 0.85,
      "freshness_flag": "current|stale|outdated"
    }
  ],
  "search_metadata": {
    "recall_count": 35,
    "rerank_count": 10,
    "avg_relevance": 0.82
  }
}
"""
```

#### DeepSearch with Cost Monitoring
```
DEEPSEARCH_CONFIG = {
    "search_domains": [
        "patent_databases",
        "academic_papers", 
        "news_articles",
        "social_media_trends",
        "regulatory_filings"
    ],
    "cost_controls": {
        "max_api_calls_per_query": 20,
        "timeout_seconds": 30,
        "result_cache_ttl": 3600
    },
    "quality_filters": {
        "min_confidence": 0.7,
        "max_results_per_domain": 5,
        "freshness_weight": 0.3
    },
    "citation_tracking": {
        "include_date_retrieved": True,
        "include_search_params": True,
        "track_cost_per_source": True
    }
}
```

## 3. Implementation Architecture

### 3.1 Agent Specialization with Cost Monitoring
```python
AGENT_CONFIG = {
    "vision_agent": {
        "role": "Vision Statement Specialist",
        "tools": ["vision_framework", "inspiration_db", "competitor_analysis"],
        "prompt_template": "SYSTEM_PROMPT_VISION_STATEMENT",
        "cost_limits": {"max_tokens": 2000, "max_api_calls": 5},
        "output_schema": "VISION_STATEMENT_SCHEMA"
    },
    "market_agent": {
        "role": "Market Timing Analyst", 
        "tools": ["rag_system", "deepsearch", "trend_analysis"],
        "prompt_template": "SYSTEM_PROMPT_TIMING_ANALYSIS",
        "cost_limits": {"max_tokens": 3000, "max_api_calls": 10},
        "parallel_capable": True
    },
    "tam_agent": {
        "role": "TAM Calculator",
        "tools": ["market_databases", "financial_models", "benchmark_data"],
        "prompt_template": "SYSTEM_PROMPT_TAM_CALCULATOR",
        "cost_limits": {"max_tokens": 4000, "max_api_calls": 15},
        "output_schema": "TAM_CALCULATOR_SCHEMA",
        "parallel_capable": True
    }
}
```

### 3.2 Task Orchestration
```python
TASK_ORCHESTRATION = {
    "parallel_groups": [
        {
            "group_id": "market_analysis",
            "tasks": ["tam_calculation", "timing_analysis"],
            "prerequisites": ["market_intelligence_complete"],
            "estimated_time": 120  # seconds
        },
        {
            "group_id": "vision_development", 
            "tasks": ["vision_statement", "problem_brief"],
            "prerequisites": ["customer_info_complete"],
            "estimated_time": 90
        }
    ],
    "serial_dependencies": [
        {"task": "exit_strategy", "depends_on": ["tam_calculation"]},
        {"task": "final_validation", "depends_on": ["all_components"]}
    ]
}
```

### 3.3 Cost Monitoring System
```python
COST_MONITOR_CONFIG = {
    "token_limits": {
        "per_component": 3000,
        "total_workflow": 20000,
        "emergency_cutoff": 25000
    },
    "cost_tracking": {
        "track_per_agent": True,
        "track_per_component": True,
        "real_time_alerts": True
    },
    "optimization_rules": {
        "cache_similar_queries": True,
        "batch_api_calls": True,
        "compress_chain_of_thought": True
    }
}
```

## 4. User Interface Patterns

### 4.1 Smart Completion Interface
```javascript
// Example UI component
const CompletionTracker = {
  categories: {
    problem_clarity: { progress: 0.85, status: "complete" },
    market_context: { progress: 0.60, status: "in_progress" },
    solution_uniqueness: { progress: 0.90, status: "complete" },
    scale_potential: { progress: 0.40, status: "needs_input" },
    execution_readiness: { progress: 0.75, status: "sufficient" }
  },
  overall_progress: 0.70,
  can_proceed: false,
  can_skip: true,
  skip_reason: "8 questions asked - you can proceed with current information"
}
```

### 4.2 Output Templates with Metadata
```
EXECUTIVE_SUMMARY_TEMPLATE = """
# Vision & Opportunity Assessment

## Vision Statement
{vision_statement}
*Confidence: {vision_confidence}/10 | Last updated: {vision_timestamp}*

## Problem/Mission Brief  
{problem_brief}
*Sources: {problem_sources} | Freshness: {problem_freshness}*

## Market Opportunity
- **Market Size**: {tam_summary}
- **Timing**: {timing_score}/10 - {timing_rationale}
- **Exit Potential**: {exit_summary}

## Key Insights
{key_insights}

## Data Quality Report
- **Total Citations**: {total_citations}
- **Fresh Data**: {fresh_citations} sources
- **Stale Data**: {stale_citations} sources (flagged for refresh)
- **Completion Level**: {completion_percentage}%

## Cost Summary
- **Tokens Used**: {total_tokens}
- **Processing Time**: {processing_time}s
- **API Calls**: {api_calls}

## Recommended Next Steps
{next_steps}

---
*Generated by AI Startup Framework v2.0*
*Quality Score: {quality_score}/10*
*Last updated: {timestamp}*
"""
```

This comprehensive framework provides robust information gathering with clear completion rules, parallel processing for efficiency, transparent quality metrics, universal JSON schema validation, comprehensive citation tracking, and cost monitoring throughout the entire workflow. 