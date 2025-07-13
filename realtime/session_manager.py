import asyncio
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages Realtime API sessions and tool integration"""
    
    def __init__(self):
        self.active_sessions = {}
        self.tool_schemas = self._get_tool_schemas()
    
    def _get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all available tools"""
        schemas = []
        
        # Product Market Fit Analysis Tool
        schemas.append({
            "type": "function",
            "name": "product_market_fit_tool",
            "description": "Analyze product market fit, lead quality, market segments, and business intelligence using HubSpot contacts and Notion product data",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's analysis request or question"
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Optional parameters for the analysis",
                        "properties": {
                            "analysis_type": {
                                "type": "string",
                                "enum": ["segments", "lead_quality", "market_fit", "strategy", "comprehensive"],
                                "description": "Type of analysis to perform"
                            },
                            "context": {
                                "type": "string",
                                "description": "Context for the analysis (e.g., 'Análise de segmentação de mercado')"
                            }
                        }
                    }
                },
                "required": ["query"]
            }
        })
        
        # Specific analysis tools
        schemas.append({
            "type": "function",
            "name": "get_contact_segments",
            "description": "Get detailed analysis of contact segments from HubSpot data",
            "parameters": {
                "type": "object",
                "properties": {
                    "parameters": {
                        "type": "object",
                        "description": "Optional parameters for segment analysis"
                    }
                }
            }
        })
        
        schemas.append({
            "type": "function",
            "name": "get_lead_quality_analysis",
            "description": "Analyze lead quality and identify most promising prospects",
            "parameters": {
                "type": "object",
                "properties": {
                    "parameters": {
                        "type": "object",
                        "description": "Optional parameters for lead quality analysis"
                    }
                }
            }
        })
        
        schemas.append({
            "type": "function",
            "name": "get_market_fit_analysis",
            "description": "Analyze product market fit based on contact data and product information",
            "parameters": {
                "type": "object",
                "properties": {
                    "parameters": {
                        "type": "object",
                        "description": "Optional parameters for market fit analysis"
                    }
                }
            }
        })
        
        schemas.append({
            "type": "function",
            "name": "get_marketing_strategy",
            "description": "Get marketing strategy recommendations based on contact and product data",
            "parameters": {
                "type": "object",
                "properties": {
                    "parameters": {
                        "type": "object",
                        "description": "Optional parameters for strategy analysis"
                    }
                }
            }
        })
        
        # Data Verification Tool
        schemas.append({
            "type": "function",
            "name": "verify_data_tool",
            "description": "Verify and analyze sales data from HubSpot CRM using AI analysis",
            "parameters": {
                "type": "object",
                "properties": {
                    "context": {
                        "type": "string",
                        "description": "Context for the data analysis (e.g., 'Sales data analysis', 'Revenue verification')"
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Specific question or analysis request about the sales data"
                    }
                },
                "required": ["context", "prompt"]
            }
        })
        
        return schemas
    
    def _handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool function calls"""
        try:
            if tool_name == "product_market_fit_tool":
                return self._call_product_market_fit_tool(arguments)
            elif tool_name == "get_contact_segments":
                return self._call_get_contact_segments(arguments)
            elif tool_name == "get_lead_quality_analysis":
                return self._call_get_lead_quality_analysis(arguments)
            elif tool_name == "get_market_fit_analysis":
                return self._call_get_market_fit_analysis(arguments)
            elif tool_name == "get_marketing_strategy":
                return self._call_get_marketing_strategy(arguments)
            elif tool_name == "verify_data_tool":
                return self._call_verify_data_tool(arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
                
        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {e}")
            return {"error": f"Tool execution failed: {str(e)}"}
    
    def _call_product_market_fit_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the main product market fit analysis tool"""
        from realtime.tools import product_market_fit_tool
        
        query = arguments.get("query", "")
        parameters = arguments.get("parameters", {})
        
        return self._run_async_tool(product_market_fit_tool, query, parameters)
    
    def _call_get_contact_segments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the contact segments analysis tool"""
        from realtime.tools import get_contact_segments
        
        parameters = arguments.get("parameters", {})
        
        return self._run_async_tool(get_contact_segments, parameters)
    
    def _call_get_lead_quality_analysis(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the lead quality analysis tool"""
        from realtime.tools import get_lead_quality_analysis
        
        parameters = arguments.get("parameters", {})
        
        return self._run_async_tool(get_lead_quality_analysis, parameters)
    
    def _call_get_market_fit_analysis(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the market fit analysis tool"""
        from realtime.tools import get_market_fit_analysis
        
        parameters = arguments.get("parameters", {})
        
        return self._run_async_tool(get_market_fit_analysis, parameters)
    
    def _call_get_marketing_strategy(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the marketing strategy tool"""
        from realtime.tools import get_marketing_strategy
        
        parameters = arguments.get("parameters", {})
        
        return self._run_async_tool(get_marketing_strategy, parameters)
    
    def _call_verify_data_tool(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call the data verification tool"""
        from realtime.tools import verify_data_tool
        
        context = arguments.get("context", "General data verification")
        prompt = arguments.get("prompt", "Analyze the sales data")
        
        return self._run_async_tool(verify_data_tool, context, prompt)
    
    def _run_async_tool(self, tool_func, *args) -> Dict[str, Any]:
        """Run an async tool function"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(tool_func(*args))
                return result
            finally:
                loop.close()
        except Exception as e:
            logger.error(f"Async tool execution failed: {e}")
            return {
                "success": False,
                "error": f"Tool execution failed: {str(e)}"
            }
    
    def create_session(self, session_id: str, config: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new session"""
        session_config = {
            "session_id": session_id,
            "tools": self.tool_schemas,
            "created_at": asyncio.get_event_loop().time(),
            "config": config or {}
        }
        
        self.active_sessions[session_id] = session_config
        
        return {
            "success": True,
            "session": session_config
        }
    
    def get_session(self, session_id: str) -> Dict[str, Any]:
        """Get session information"""
        if session_id in self.active_sessions:
            return {
                "success": True,
                "session": self.active_sessions[session_id]
            }
        else:
            return {
                "success": False,
                "error": "Session not found"
            }
    
    def end_session(self, session_id: str) -> Dict[str, Any]:
        """End a session"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            return {
                "success": True,
                "message": "Session ended successfully"
            }
        else:
            return {
                "success": False,
                "error": "Session not found"
            }
    
    def list_sessions(self) -> Dict[str, Any]:
        """List all active sessions"""
        return {
            "success": True,
            "sessions": list(self.active_sessions.keys()),
            "count": len(self.active_sessions)
        }
    
    def handle_message(self, session_id: str, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming message for a session"""
        if session_id not in self.active_sessions:
            return {
                "success": False,
                "error": "Session not found"
            }
        
        # Handle tool calls
        if message.get("type") == "tool_call":
            tool_name = message.get("tool_name")
            arguments = message.get("arguments", {})
            
            result = self._handle_tool_call(tool_name, arguments)
            
            return {
                "success": True,
                "type": "tool_response",
                "tool_name": tool_name,
                "result": result
            }
        
        # Handle other message types
        return {
            "success": True,
            "type": "message_received",
            "session_id": session_id,
            "message": message
        }


# Global session manager instance
session_manager = SessionManager() 