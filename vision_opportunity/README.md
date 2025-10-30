# Vision & Opportunity Playbook - Console Application

A first-version console application implementing the AI-Powered Startup Framework for developing comprehensive vision statements and opportunity assessments.

## Features

🚀 **Smart Information Gathering**
- Interactive questioning system with completion tracking
- 80% completion threshold with "Skip for now" option
- Real-time progress monitoring across 5 categories

🧠 **AI-Powered Analysis**
- Parallel task execution for faster results
- Vision statement generation with multiple variations
- TAM calculation using multiple methodologies
- Market timing analysis using TIMING framework
- Exit strategy development

📊 **Professional Output**
- Beautiful console interface using Rich library
- Markdown report generation
- Cost monitoring and optimization
- JSON schema validation throughout

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone or download the application files**
   ```bash
   cd vision_opportunity
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: Create configuration file**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Make executable (optional)**
   ```bash
   chmod +x main.py
   ```

## Usage

### Basic Usage

Run the main workflow:
```bash
python main.py
```

Or if made executable:
```bash
./main.py
```

### Command Line Options

```bash
python main.py --help
```

Options:
- `--debug` - Enable debug mode for detailed error messages
- `--config PATH` - Specify custom configuration file (default: .env)
- `--version` - Show version information

### CLI Tools

Check application status:
```bash
python main.py status
```

Validate an assessment file:
```bash
python main.py validate vision_opportunity_assessment.md
```

Run demo mode:
```bash
python main.py demo
```

## Workflow Process

### Phase 1: Information Gathering
- Interactive questioning across 5 categories:
  - **Problem Clarity**: Understanding the core problem
  - **Market Context**: Industry and timing factors
  - **Solution Uniqueness**: Differentiation and value proposition
  - **Scale Potential**: Market size and growth
  - **Execution Readiness**: Founder-market fit

### Phase 2: Analysis & Synthesis
- **Parallel Tasks**: Vision statement generation, TAM calculation, timing analysis
- **Serial Tasks**: Exit strategy development (depends on TAM)
- **Real-time Progress**: Visual progress bars and status updates

### Phase 3: Output Generation
- **Vision Statement**: 3 variations with different tones
- **TAM Analysis**: Top-down and bottom-up calculations
- **Market Timing**: TIMING framework analysis
- **Exit Strategy**: Strategic exit considerations
- **Markdown Report**: Professional documentation

## File Structure

```
vision_opportunity/
├── main.py              # Main application entry point
├── models.py            # Data models and Pydantic schemas
├── agents.py            # AI agent implementations
├── workflow.py          # Workflow orchestration
├── ui.py               # Console UI components
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── .env.example        # Example configuration
└── ai_workflow_map_and_prompt_library.md  # Technical documentation
```

## Generated Output

The application generates several files:

1. **`vision_opportunity_assessment.md`** - Main assessment report
2. **`workflow_state.json`** - Debug information about the session
3. **Console output** - Real-time progress and results

### Sample Assessment Structure

```markdown
# Vision & Opportunity Assessment

## Executive Summary
Brief overview of the assessment results.

## Vision Statement
**Recommended Vision:** [Generated vision statement]
**Reasoning:** [Why this vision was recommended]

### Alternative Variations:
1. **Ambitious:** [Vision with inspiring tone]
2. **Practical:** [Vision with practical tone]
3. **Disruptive:** [Vision with disruptive tone]

## Total Addressable Market
### TAM Range
- **Conservative:** $X,XXX,XXX
- **Recommended:** $X,XXX,XXX
- **Optimistic:** $X,XXX,XXX

## Market Timing Analysis
[Analysis using TIMING framework]

## Exit Strategy
[Strategic exit considerations]

## Next Steps
[Recommended actions]
```

## Configuration

### Environment Variables

Create a `.env` file for configuration:

```env
# Application Settings
DEBUG=false
LOG_LEVEL=INFO

# Cost Limits
MAX_TOKENS=20000
MAX_API_CALLS=50
MAX_COMPUTATION_TIME=300

# Output Settings
OUTPUT_FORMAT=markdown
EXPORT_DIRECTORY=./exports

# AI Settings (for future API integration)
# OPENAI_API_KEY=your_api_key_here
# MODEL_NAME=gpt-4
```

## Architecture

### Core Components

1. **Models** (`models.py`)
   - Pydantic data models for type safety
   - JSON schema validation
   - Workflow state management

2. **Agents** (`agents.py`)
   - Specialized AI agents for each component
   - Cost tracking and monitoring
   - Mock implementations for demonstration

3. **Workflow** (`workflow.py`)
   - Orchestrates the entire process
   - Manages state transitions
   - Handles parallel/serial task execution

4. **UI** (`ui.py`)
   - Rich console interface
   - Progress visualization
   - Interactive questioning

### Design Patterns

- **Agent Pattern**: Each component has a specialized agent
- **State Machine**: Workflow progresses through defined phases
- **Observer Pattern**: UI updates based on state changes
- **Strategy Pattern**: Multiple TAM calculation methods

## Extending the Application

### Adding New Question Categories

1. Add to `QuestionCategory` enum in `models.py`
2. Update `WorkflowState` default categories
3. Add question templates in `QuestionGeneratorAgent`
4. Update progress calculation logic

### Adding New Agents

1. Inherit from `BaseAgent` in `agents.py`
2. Implement required methods
3. Add to `WorkflowCoordinatorAgent.agents`
4. Update workflow orchestration

### Adding Real AI Integration

Replace mock implementations with actual API calls:

```python
# In agents.py
import openai

class VisionStatementAgent(BaseAgent):
    def generate_vision_statement(self, workflow_state):
        # Replace mock with actual OpenAI API call
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": VISION_PROMPT}]
        )
        return parse_response(response)
```

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Code Quality

```bash
# Type checking
mypy vision_opportunity/

# Code formatting
black vision_opportunity/

# Linting
flake8 vision_opportunity/
```

### Development Mode

Run with debug flag for detailed error messages:
```bash
python main.py --debug
```

## Troubleshooting

### Common Issues

1. **ImportError: No module named 'rich'**
   ```bash
   pip install rich
   ```

2. **Permission denied**
   ```bash
   chmod +x main.py
   ```

3. **Pydantic validation errors**
   - Check data types in responses
   - Verify JSON schema compatibility

### Getting Help

1. Check application status:
   ```bash
   python main.py status
   ```

2. Run with debug mode:
   ```bash
   python main.py --debug
   ```

3. Validate output files:
   ```bash
   python main.py validate vision_opportunity_assessment.md
   ```

## Roadmap

### Version 1.1 (Next)
- [ ] Real AI API integration
- [ ] Enhanced validation
- [ ] Export to PDF/HTML
- [ ] Demo mode with sample data

### Version 1.2 (Future)
- [ ] Web interface
- [ ] Database storage
- [ ] Multi-user support
- [ ] Advanced analytics

### Version 2.0 (Long-term)
- [ ] Full framework implementation
- [ ] All 14 playbooks
- [ ] Advanced AI capabilities
- [ ] Enterprise features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is part of the AI-Powered Startup Framework.

---

**Ready to build your vision?** 🚀

```bash
python main.py
``` 