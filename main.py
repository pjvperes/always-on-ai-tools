#!/usr/bin/env python3
"""
Voice Assistant with Product Market Fit Integration
Main entry point for the voice assistant with proactive triggers and realtime API.
"""

import asyncio
import logging
import signal
import sys
from typing import Dict, Any, List

# Import configuration
from config import (
    TRIGGER_CONFIG, 
    REALTIME_CONFIG, 
    LOGGING_CONFIG, 
    PRODUCT_MARKET_FIT_CONFIG,
    FEATURE_FLAGS,
    validate_config
)

# Import trigger system
from triggers.base import BaseTrigger
from triggers.builtin.product_market_fit_trigger import ProductMarketFitTrigger

# Import realtime system
from realtime.session_manager import SessionManager

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG["level"]),
    format=LOGGING_CONFIG["format"]
)
logger = logging.getLogger(__name__)


class TriggerManager:
    """Manages all proactive triggers"""
    
    def __init__(self):
        self.triggers: List[BaseTrigger] = []
        self.enabled = True
    
    def add_trigger(self, trigger: BaseTrigger):
        """Add a trigger to the manager"""
        self.triggers.append(trigger)
        # Sort by priority (higher priority first)
        self.triggers.sort(key=lambda t: t.priority, reverse=True)
        logger.info(f"Added trigger: {trigger}")
    
    def remove_trigger(self, trigger_class: type):
        """Remove a trigger by class type"""
        self.triggers = [t for t in self.triggers if not isinstance(t, trigger_class)]
        logger.info(f"Removed trigger: {trigger_class.__name__}")
    
    def process_query(self, query: str, **kwargs) -> Dict[str, Any]:
        """Process a query through all triggers"""
        if not self.enabled:
            return {
                "success": False,
                "error": "Trigger system is disabled"
            }
        
        logger.info(f"Processing query: '{query}'")
        
        # Find matching triggers
        matching_triggers = []
        for trigger in self.triggers:
            if trigger.matches(query):
                matching_triggers.append(trigger)
        
        if not matching_triggers:
            return {
                "success": False,
                "error": "No matching triggers found",
                "query": query
            }
        
        # Execute the highest priority trigger
        selected_trigger = matching_triggers[0]
        logger.info(f"Selected trigger: {selected_trigger}")
        
        try:
            result = selected_trigger.action(query, **kwargs)
            return {
                "success": True,
                "trigger": selected_trigger.__class__.__name__,
                "result": result
            }
        except Exception as e:
            logger.error(f"Trigger execution failed: {e}")
            return {
                "success": False,
                "error": f"Trigger execution failed: {str(e)}",
                "trigger": selected_trigger.__class__.__name__
            }
    
    def list_triggers(self) -> List[Dict[str, Any]]:
        """List all registered triggers"""
        return [
            {
                "name": trigger.__class__.__name__,
                "priority": trigger.priority,
                "keywords": trigger.keywords,
                "criteria": trigger.activation_criteria
            }
            for trigger in self.triggers
        ]


class VoiceAssistant:
    """Main voice assistant application"""
    
    def __init__(self):
        self.trigger_manager = TriggerManager()
        self.session_manager = SessionManager()
        self.running = False
        
        # Load configuration
        self.load_configuration()
        
        # Load triggers
        self.load_triggers()
    
    def load_configuration(self):
        """Load and validate configuration"""
        try:
            validate_config()
            logger.info("Configuration validation passed")
        except ValueError as e:
            logger.error(f"Configuration validation failed: {e}")
            sys.exit(1)
    
    def load_triggers(self):
        """Load all enabled triggers"""
        enabled_triggers = TRIGGER_CONFIG["enabled_triggers"]
        
        # Load Product Market Fit trigger
        if "product_market_fit_trigger" in enabled_triggers:
            if PRODUCT_MARKET_FIT_CONFIG["enabled"]:
                self.trigger_manager.add_trigger(ProductMarketFitTrigger())
                logger.info("Product Market Fit trigger loaded")
            else:
                logger.warning("Product Market Fit trigger is disabled in configuration")
        
        # Load other triggers (placeholders)
        if "assistant_trigger" in enabled_triggers:
            logger.info("Assistant trigger would be loaded here")
        
        if "weather_trigger" in enabled_triggers:
            logger.info("Weather trigger would be loaded here")
        
        if "search_trigger" in enabled_triggers:
            logger.info("Search trigger would be loaded here")
        
        if "test_trigger" in enabled_triggers:
            logger.info("Test trigger would be loaded here")
    
    def process_voice_input(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process voice input through the trigger system"""
        context = context or {}
        
        # Add timing information
        import time
        start_time = time.time()
        
        result = self.trigger_manager.process_query(query, context=context)
        
        # Add performance metrics
        result["processing_time"] = time.time() - start_time
        result["timestamp"] = time.time()
        
        return result
    
    def create_realtime_session(self, session_id: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new realtime API session"""
        return self.session_manager.create_session(session_id, config)
    
    def handle_realtime_message(self, session_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a realtime API message"""
        return self.session_manager.handle_message(session_id, message)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status information"""
        return {
            "running": self.running,
            "triggers": {
                "count": len(self.trigger_manager.triggers),
                "enabled": self.trigger_manager.enabled,
                "list": self.trigger_manager.list_triggers()
            },
            "realtime_sessions": self.session_manager.list_sessions(),
            "configuration": {
                "product_market_fit_enabled": PRODUCT_MARKET_FIT_CONFIG["enabled"],
                "feature_flags": FEATURE_FLAGS
            }
        }
    
    def start(self):
        """Start the voice assistant"""
        logger.info("Starting Voice Assistant with Product Market Fit Integration")
        self.running = True
        
        # Print system status
        status = self.get_system_status()
        logger.info(f"System Status: {status}")
        
        # Start main loop
        try:
            asyncio.run(self.main_loop())
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt, shutting down...")
            self.stop()
    
    def stop(self):
        """Stop the voice assistant"""
        logger.info("Stopping Voice Assistant")
        self.running = False
    
    async def main_loop(self):
        """Main application loop"""
        logger.info("Voice Assistant is running...")
        logger.info("Available commands:")
        logger.info("  - Say 'product market fit analysis' to trigger PMF analysis")
        logger.info("  - Say 'analyze lead quality' to analyze leads")
        logger.info("  - Say 'hey bot' to start assistant mode")
        logger.info("  - Press Ctrl+C to stop")
        
        while self.running:
            try:
                # Simulate voice input for demonstration
                # In a real implementation, this would be replaced with actual voice processing
                await asyncio.sleep(1)
                
                # You can test with:
                # result = self.process_voice_input("analyze product market fit")
                # print(f"Result: {result}")
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                await asyncio.sleep(1)
    
    def demo_mode(self):
        """Run in demo mode for testing"""
        logger.info("Running in demo mode")
        
        # Test queries
        test_queries = [
            "analyze product market fit",
            "show me lead quality analysis",
            "what segments are most promising",
            "give me marketing strategy recommendations",
            "hubspot contact analysis"
        ]
        
        for query in test_queries:
            logger.info(f"\n--- Testing query: '{query}' ---")
            result = self.process_voice_input(query)
            logger.info(f"Result: {result}")
            
            if result["success"] and "result" in result:
                response = result["result"]
                if "text" in response:
                    logger.info(f"Response: {response['text'][:200]}...")


def signal_handler(signum, frame):
    """Handle system signals"""
    logger.info(f"Received signal {signum}")
    sys.exit(0)


def main():
    """Main entry point"""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start the voice assistant
    assistant = VoiceAssistant()
    
    # Check if demo mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        assistant.demo_mode()
    else:
        assistant.start()


if __name__ == "__main__":
    main() 