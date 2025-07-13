import requests
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


async def product_market_fit_tool(query: str, parameters: dict = None) -> dict:
    """
    Product Market Fit Analysis Tool for the assistant
    
    Args:
        query: User's request
        parameters: Optional parameters extracted from the conversation
    
    Returns:
        Dict with tool execution result
    """
    try:
        # Get API configuration
        api_url = os.getenv("PRODUCT_MARKET_FIT_API_URL", "http://localhost:8000")
        
        # Extract context and prompt from parameters
        context = parameters.get("context", "Análise de produto e mercado") if parameters else "Análise de produto e mercado"
        analysis_type = parameters.get("analysis_type", "comprehensive") if parameters else "comprehensive"
        
        # Refine the prompt based on the query and analysis type
        prompt = _refine_prompt_for_assistant(query, analysis_type)
        
        logger.info(f"Product Market Fit tool called with query: {query}")
        
        # Call the API
        response = requests.post(
            f"{api_url}/dashboard/data",
            headers={"Content-Type": "application/json"},
            json={
                "context": context,
                "prompt": prompt
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Format the response for the assistant
            formatted_response = _format_assistant_response(data)
            
            return {
                "success": True,
                "result": formatted_response["summary"],
                "details": formatted_response["details"],
                "data": {
                    "contacts_analyzed": len(data.get("hubspot_contacts", [])),
                    "llm_response": data.get("llm_response", "")
                }
            }
        else:
            return {
                "success": False,
                "error": f"API returned status {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "The analysis request timed out. The service may be processing a large dataset."
        }
    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "error": "Could not connect to the Product Market Fit analysis service. Please ensure it's running on the configured URL."
        }
    except Exception as e:
        logger.error(f"Product Market Fit tool error: {e}")
        return {
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }


def _refine_prompt_for_assistant(query: str, analysis_type: str) -> str:
    """Refine the user's query into a specific prompt for the LLM"""
    query_lower = query.lower()
    
    # Map analysis types to specific prompts
    if analysis_type == "segments":
        return "Identifique e analise os principais segmentos de empresa na nossa base de contatos. Para cada segmento, forneça: características principais, tamanho do mercado, potencial de conversão e estratégias recomendadas."
    
    elif analysis_type == "lead_quality":
        return "Avalie a qualidade dos leads em nossa base de contatos. Identifique os 5 mais promissores, explique os critérios de qualificação e sugira próximos passos para cada um."
    
    elif analysis_type == "market_fit":
        return "Analise o product market fit com base nos dados de contatos e informações do produto. Identifique padrões de ajuste produto-mercado, gaps e oportunidades de crescimento."
    
    elif analysis_type == "strategy":
        return "Com base na análise dos contatos e dados do produto, desenvolva uma estratégia de marketing e vendas. Inclua recomendações específicas para cada segmento principal."
    
    else:
        # Default comprehensive analysis based on query content
        if "segment" in query_lower:
            return "Faça uma análise detalhada dos segmentos de mercado presentes na nossa base de contatos."
        elif "lead" in query_lower and "quality" in query_lower:
            return "Avalie a qualidade dos leads e identifique os mais promissores."
        elif "strategy" in query_lower:
            return "Sugira uma estratégia de marketing baseada nos dados disponíveis."
        elif "fit" in query_lower or "pmf" in query_lower:
            return "Analise o product market fit com base nos dados de contatos."
        else:
            return "Faça uma análise abrangente dos nossos contatos e identifique insights-chave sobre product market fit, segmentação e oportunidades de crescimento."


def _format_assistant_response(data: Dict[str, Any]) -> Dict[str, str]:
    """Format the API response for the assistant"""
    try:
        llm_response = data.get("llm_response", "")
        contacts_count = len(data.get("hubspot_contacts", []))
        
        if llm_response:
            # Create a summary (first paragraph or key points)
            lines = llm_response.split('\n')
            summary_lines = []
            
            for line in lines:
                if line.strip():
                    summary_lines.append(line.strip())
                    if len(summary_lines) >= 3:  # Keep summary concise
                        break
            
            summary = " ".join(summary_lines)
            
            # Clean the summary
            summary = summary.replace("**", "").replace("*", "")
            summary = summary.replace("Com base na análise", "Based on the analysis")
            
            # Create detailed response
            details = f"Analysis based on {contacts_count} contacts from HubSpot and product information from Notion.\n\n{llm_response}"
            
            return {
                "summary": summary,
                "details": details
            }
        else:
            return {
                "summary": f"Analyzed {contacts_count} contacts but couldn't generate specific insights.",
                "details": "The analysis completed but no detailed insights were generated. Please try rephrasing your request."
            }
            
    except Exception as e:
        logger.error(f"Error formatting assistant response: {e}")
        return {
            "summary": "Analysis completed but had trouble formatting results.",
            "details": "There was an error processing the analysis results. Please try again."
        }


# Additional utility functions for the assistant
async def get_contact_segments(parameters: dict = None) -> dict:
    """Get contact segments analysis"""
    return await product_market_fit_tool(
        "Analyze contact segments", 
        {"analysis_type": "segments", "context": "Análise de segmentação de contatos"}
    )


async def get_lead_quality_analysis(parameters: dict = None) -> dict:
    """Get lead quality analysis"""
    return await product_market_fit_tool(
        "Analyze lead quality", 
        {"analysis_type": "lead_quality", "context": "Análise de qualidade de leads"}
    )


async def get_market_fit_analysis(parameters: dict = None) -> dict:
    """Get product market fit analysis"""
    return await product_market_fit_tool(
        "Analyze product market fit", 
        {"analysis_type": "market_fit", "context": "Análise de product market fit"}
    )


async def get_marketing_strategy(parameters: dict = None) -> dict:
    """Get marketing strategy recommendations"""
    return await product_market_fit_tool(
        "Develop marketing strategy", 
        {"analysis_type": "strategy", "context": "Estratégia de marketing e vendas"}
    ) 

async def verify_data_tool(context: str, prompt: str) -> dict:
    """
    Verify and analyze sales data from HubSpot CRM
    
    Args:
        context: Context for the data analysis
        prompt: Specific question or analysis request
    
    Returns:
        Dict with tool execution result
    """
    import httpx
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    try:
        # Check if required API keys are configured
        hubspot_api_key = os.getenv("HUBSPOT_API_KEY")
        openai_api_key = os.getenv("OPENAI_API_KEY")
        api_base_url = os.getenv("VERIFY_DATA_API_URL", "http://localhost:8000")
        
        if not hubspot_api_key or not openai_api_key:
            return {
                "success": False,
                "error": "API keys not configured. Please set HUBSPOT_API_KEY and OPENAI_API_KEY in .env file"
            }
        
        # Call the verify_data API
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "context": context,
                "prompt": prompt
            }
            
            response = await client.post(
                f"{api_base_url}/verify-data",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("error"):
                    return {
                        "success": False,
                        "error": data["error"]
                    }
                
                return {
                    "success": True,
                    "result": data.get("response", "Data verification completed"),
                    "details": "Analysis completed using HubSpot CRM data"
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}: {response.text}"
                }
            
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Request timed out. Please try again."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Tool execution failed: {str(e)}"
        } 