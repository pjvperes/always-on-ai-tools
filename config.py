import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Product Market Fit API Configuration
PRODUCT_MARKET_FIT_CONFIG = {
    "api_url": os.getenv("PRODUCT_MARKET_FIT_API_URL", "http://localhost:8000"),
    "timeout": int(os.getenv("PRODUCT_MARKET_FIT_TIMEOUT", "30")),
    "enabled": os.getenv("PRODUCT_MARKET_FIT_ENABLED", "true").lower() == "true"
}

# Trigger Configuration
TRIGGER_CONFIG = {
    "enabled_triggers": [
        "assistant_trigger",
        "test_trigger", 
        "weather_trigger",
        "search_trigger",
        "product_market_fit_trigger",  # Add the new trigger
        "verify_data_trigger",  # Add the data verification trigger
    ],
    "trigger_priorities": {
        "assistant_trigger": 100,
        "verify_data_trigger": 75,
        "product_market_fit_trigger": 75,
        "weather_trigger": 70,
        "search_trigger": 60,
        "test_trigger": 50,
    }
}

# Realtime API Configuration
REALTIME_CONFIG = {
    "enabled_tools": [
        "product_market_fit_tool",
        "get_contact_segments",
        "get_lead_quality_analysis",
        "get_market_fit_analysis",
        "get_marketing_strategy",
        "verify_data_tool",
    ],
    "session_timeout": int(os.getenv("REALTIME_SESSION_TIMEOUT", "3600")),  # 1 hour
    "max_concurrent_sessions": int(os.getenv("REALTIME_MAX_SESSIONS", "10"))
}

# Voice Assistant Configuration
VOICE_CONFIG = {
    "default_voice": os.getenv("DEFAULT_VOICE", "alloy"),
    "default_speed": float(os.getenv("DEFAULT_SPEED", "1.0")),
    "language": os.getenv("VOICE_LANGUAGE", "en-US"),
    "business_analysis_voice": {
        "voice": "alloy",
        "speed": 0.9  # Slightly slower for business content
    }
}

# Logging Configuration
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO"),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "handlers": {
        "console": True,
        "file": {
            "enabled": os.getenv("LOG_TO_FILE", "false").lower() == "true",
            "filename": os.getenv("LOG_FILE", "voice_assistant.log"),
            "max_size": int(os.getenv("LOG_MAX_SIZE", "10485760")),  # 10MB
            "backup_count": int(os.getenv("LOG_BACKUP_COUNT", "3"))
        }
    }
}

# API Keys and Environment Variables
API_KEYS = {
    "hubspot": os.getenv("HUBSPOT_API_KEY"),
    "notion": os.getenv("NOTION_API_KEY"),
    "openai": os.getenv("OPENAI_API_KEY"),
    "product_market_fit": os.getenv("PRODUCT_MARKET_FIT_API_KEY")  # If API key is needed
}

# Validate required environment variables
def validate_config():
    """Validate that all required configuration is present"""
    required_vars = []
    missing_vars = []
    
    # Check if Product Market Fit integration is enabled
    if PRODUCT_MARKET_FIT_CONFIG["enabled"]:
        required_vars.extend([
            "HUBSPOT_API_KEY",
            "NOTION_API_KEY", 
            "OPENAI_API_KEY"
        ])
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True

# Feature Flags
FEATURE_FLAGS = {
    "product_market_fit_enabled": PRODUCT_MARKET_FIT_CONFIG["enabled"],
    "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
    "verbose_logging": os.getenv("VERBOSE_LOGGING", "false").lower() == "true",
    "performance_monitoring": os.getenv("PERFORMANCE_MONITORING", "false").lower() == "true"
}

# Performance Settings
PERFORMANCE_CONFIG = {
    "max_response_time": int(os.getenv("MAX_RESPONSE_TIME", "30")),  # seconds
    "cache_enabled": os.getenv("CACHE_ENABLED", "true").lower() == "true",
    "cache_ttl": int(os.getenv("CACHE_TTL", "300")),  # 5 minutes
    "retry_attempts": int(os.getenv("RETRY_ATTEMPTS", "3")),
    "retry_delay": float(os.getenv("RETRY_DELAY", "1.0"))
}

# Security Configuration
SECURITY_CONFIG = {
    "rate_limiting": {
        "enabled": os.getenv("RATE_LIMITING_ENABLED", "true").lower() == "true",
        "max_requests_per_minute": int(os.getenv("MAX_REQUESTS_PER_MINUTE", "60")),
        "max_requests_per_hour": int(os.getenv("MAX_REQUESTS_PER_HOUR", "1000"))
    },
    "allowed_origins": os.getenv("ALLOWED_ORIGINS", "*").split(","),
    "api_key_required": os.getenv("API_KEY_REQUIRED", "false").lower() == "true"
}

# Export all configurations
__all__ = [
    "PRODUCT_MARKET_FIT_CONFIG",
    "TRIGGER_CONFIG", 
    "REALTIME_CONFIG",
    "VOICE_CONFIG",
    "LOGGING_CONFIG",
    "API_KEYS",
    "FEATURE_FLAGS",
    "PERFORMANCE_CONFIG",
    "SECURITY_CONFIG",
    "validate_config"
] 