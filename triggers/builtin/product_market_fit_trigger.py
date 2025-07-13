from triggers.base import BaseTrigger
import requests
import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ProductMarketFitTrigger(BaseTrigger):
    def __init__(self):
        super().__init__(
            # Keywords that will activate this trigger
            keywords=[
                "product market fit", "pmf analysis", "market analysis",
                "lead analysis", "segmento análise", "análise de mercado",
                "dashboard analysis", "hubspot analysis", "contact analysis",
                "business intelligence", "sales intelligence", "marketing insights",
                "análise de leads", "análise de contatos", "inteligência de vendas"
            ],
            
            # Priority (higher = more specific, executes first)
            priority=75,
            
            # What this trigger should respond to
            activation_criteria="User wants to analyze product market fit, leads, contacts, or business intelligence using HubSpot and Notion data",
            
            # Examples of what SHOULD trigger this
            positive_examples=[
                "Analyze product market fit for our leads",
                "Give me insights about our HubSpot contacts",
                "What segments are most promising in our database?",
                "Analyze our lead quality",
                "Show me market analysis from our contacts",
                "Faça uma análise de product market fit",
                "Analise nossos leads do HubSpot",
                "Quais segmentos são mais promissores?"
            ],
            
            # Examples of what should NOT trigger this
            negative_examples=[
                "What's the weather?",
                "Search for something online",
                "Hey bot",
                "Set a reminder",
                "Play music"
            ]
        )
        
        # API configuration
        self.api_base_url = os.getenv("PRODUCT_MARKET_FIT_API_URL", "http://localhost:8000")
        self.api_timeout = 30  # Longer timeout for data processing
    
    def action(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the product market fit analysis
        
        Args:
            query: The user's spoken text
            **kwargs: Additional context (conversation history, etc.)
        
        Returns:
            Dict with 'text', 'speak', and optional 'voice_settings'
        """
        logger.info(f"Product Market Fit trigger activated with query: {query}")
        
        try:
            # Extract context and refine prompt for better analysis
            context = self._extract_context(query)
            refined_prompt = self._refine_prompt(query)
            
            # Call the API
            response = self._call_api(context, refined_prompt)
            
            if response.get("success"):
                # Format response for voice
                voice_response = self._format_for_voice(response["data"])
                
                return {
                    "text": voice_response,
                    "speak": True,
                    "voice_settings": {
                        "voice": "alloy",
                        "speed": 0.9  # Slightly slower for business analysis
                    }
                }
            else:
                return {
                    "text": f"I couldn't complete the product market fit analysis. {response.get('error', 'Unknown error')}",
                    "speak": True
                }
                
        except requests.exceptions.Timeout:
            return {
                "text": "The market analysis is taking longer than expected. Please try again in a moment.",
                "speak": True
            }
        except requests.exceptions.ConnectionError:
            return {
                "text": "I couldn't connect to the analysis service. Please check if the product market fit tool is running.",
                "speak": True
            }
        except Exception as e:
            logger.error(f"Product Market Fit trigger error: {e}")
            return {
                "text": "Sorry, there was an error performing the market analysis. Please try again.",
                "speak": True
            }
    
    def _extract_context(self, query: str) -> str:
        """Extract or infer context from the query"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["lead", "leads", "prospects"]):
            return "Análise de leads e prospecção de clientes"
        elif any(word in query_lower for word in ["segment", "segmento", "market"]):
            return "Análise de segmentação de mercado"
        elif any(word in query_lower for word in ["contact", "contato", "cliente"]):
            return "Análise de base de contatos"
        elif any(word in query_lower for word in ["fit", "pmf", "product market"]):
            return "Análise de product market fit"
        elif any(word in query_lower for word in ["sales", "vendas", "revenue"]):
            return "Análise de vendas e receita"
        else:
            return "Análise geral de marketing e produto"
    
    def _refine_prompt(self, query: str) -> str:
        """Refine the user's query into a more specific prompt for the LLM"""
        query_lower = query.lower()
        
        # Common analysis patterns
        if "segment" in query_lower or "segmento" in query_lower:
            return "Identifique e analise os principais segmentos de empresa na nossa base de contatos. Destaque características, potencial de conversão e estratégias recomendadas para cada segmento."
        
        elif "lead" in query_lower and ("quality" in query_lower or "qualidade" in query_lower):
            return "Avalie a qualidade dos leads em nossa base de contatos. Identifique os mais promissores e sugira critérios de qualificação."
        
        elif "promising" in query_lower or "promissor" in query_lower:
            return "Identifique os 5 contatos mais promissores da nossa base e explique por que são considerados leads de alta qualidade."
        
        elif "market" in query_lower and "fit" in query_lower:
            return "Analise o product market fit com base nos dados de contatos. Identifique padrões de ajuste produto-mercado e oportunidades de crescimento."
        
        elif "strategy" in query_lower or "estratégia" in query_lower:
            return "Com base na análise dos contatos e dados do produto, sugira uma estratégia de marketing e vendas personalizada para cada segmento principal."
        
        else:
            # Default comprehensive analysis
            return "Faça uma análise abrangente dos nossos contatos e identifique insights-chave sobre product market fit, segmentação e oportunidades de crescimento."
    
    def _call_api(self, context: str, prompt: str) -> Dict[str, Any]:
        """Call the product market fit API"""
        try:
            response = requests.post(
                f"{self.api_base_url}/dashboard/data",
                headers={"Content-Type": "application/json"},
                json={
                    "context": context,
                    "prompt": prompt
                },
                timeout=self.api_timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "data": data
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _format_for_voice(self, data: Dict[str, Any]) -> str:
        """Format API response for voice output"""
        try:
            # Get the main LLM response
            llm_response = data.get("llm_response", "")
            
            # Get contact count for context
            contacts_count = len(data.get("hubspot_contacts", []))
            
            # Format for voice - make it more conversational and concise
            if llm_response:
                # Add contact count context
                intro = f"Based on analysis of {contacts_count} contacts from HubSpot and our product information, here's what I found:\n\n"
                
                # Clean up the response for voice
                cleaned_response = self._clean_response_for_voice(llm_response)
                
                return intro + cleaned_response
            else:
                return f"I analyzed {contacts_count} contacts but couldn't generate specific insights. Please try rephrasing your question."
                
        except Exception as e:
            logger.error(f"Error formatting response for voice: {e}")
            return "I completed the analysis but had trouble formatting the results. Please try again."
    
    def _clean_response_for_voice(self, response: str) -> str:
        """Clean and optimize response for voice output"""
        # Remove markdown formatting
        response = response.replace("**", "").replace("*", "")
        
        # Replace common symbols with words
        response = response.replace("&", "and")
        response = response.replace("%", "percent")
        response = response.replace("#", "number")
        
        # Make it more conversational
        response = response.replace("Com base na análise", "Based on my analysis")
        response = response.replace("Recomendo", "I recommend")
        response = response.replace("Sugiro", "I suggest")
        
        # Limit length for voice (keep it under 500 words)
        words = response.split()
        if len(words) > 200:
            response = " ".join(words[:200]) + "... For more detailed insights, please ask for specific aspects of the analysis."
        
        return response 