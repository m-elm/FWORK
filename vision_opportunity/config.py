"""
Configuration settings for the Vision & Opportunity Playbook.
"""

import os
from typing import Dict, Any


class Config:
    """Configuration class for the application."""
    
    def __init__(self):
        self.load_from_env()
    
    def load_from_env(self):
        """Load configuration from environment variables."""
        
        # AI Configuration
        self.use_ai = os.getenv("USE_AI", "true").lower() == "true"
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.openai_temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        self.openai_max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
        
        # Cost Limits
        self.max_tokens = int(os.getenv("MAX_TOKENS", "20000"))
        self.max_api_calls = int(os.getenv("MAX_API_CALLS", "50"))
        self.max_computation_time = int(os.getenv("MAX_COMPUTATION_TIME", "300"))
        
        # Application Settings
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        
        # Output Settings
        self.output_format = os.getenv("OUTPUT_FORMAT", "markdown")
        self.export_directory = os.getenv("EXPORT_DIRECTORY", "./exports")
        self.auto_export = os.getenv("AUTO_EXPORT", "true").lower() == "true"
        
        # UI Settings
        self.enable_progress_bars = os.getenv("ENABLE_PROGRESS_BARS", "true").lower() == "true"
        self.enable_emoji = os.getenv("ENABLE_EMOJI", "true").lower() == "true"
        self.console_width = int(os.getenv("CONSOLE_WIDTH", "120"))
        
        # Monitoring Settings
        self.enable_cost_monitoring = os.getenv("ENABLE_COST_MONITORING", "true").lower() == "true"
        self.cost_warning_threshold = float(os.getenv("COST_WARNING_THRESHOLD", "0.8"))
        self.enable_performance_tracking = os.getenv("ENABLE_PERFORMANCE_TRACKING", "true").lower() == "true"
    
    @property
    def ai_available(self) -> bool:
        """Check if AI integration is available."""
        return self.use_ai and self.openai_api_key is not None
    
    @property
    def cost_limits(self) -> Dict[str, int]:
        """Get cost limits as a dictionary."""
        return {
            "max_tokens": self.max_tokens,
            "max_api_calls": self.max_api_calls,
            "max_computation_time": self.max_computation_time
        }
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration as a dictionary."""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "temperature": self.openai_temperature,
            "max_tokens": self.openai_max_tokens
        }
    
    def print_status(self) -> str:
        """Get configuration status as a string."""
        status = []
        status.append(f"AI Integration: {'✅ Enabled' if self.ai_available else '❌ Disabled'}")
        status.append(f"Debug Mode: {'✅ Enabled' if self.debug else '❌ Disabled'}")
        status.append(f"Cost Monitoring: {'✅ Enabled' if self.enable_cost_monitoring else '❌ Disabled'}")
        status.append(f"Output Format: {self.output_format}")
        
        if self.ai_available:
            status.append(f"AI Model: {self.openai_model}")
            status.append(f"Max Tokens: {self.max_tokens:,}")
        
        return "\n".join(status)


# Global configuration instance
config = Config() 