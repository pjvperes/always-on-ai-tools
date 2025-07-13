from triggers.base import BaseTrigger
import httpx
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class VerifyDataTrigger(BaseTrigger):
    def __init__(self):
        super().__init__(
            # Keywords that will activate this trigger
            keywords=[
                "verificar dados", "verify data", "check data", "dados hubspot",
                "conferir vendas", "analisar dados", "verificar vendas", "check sales",
                "dados do crm", "crm data", "hubspot data", "sales data"
            ],
            
            # Priority (higher = more specific, executes first)
            priority=75,  # High priority for data verification
            
            # What this trigger should respond to
            activation_criteria="User wants to verify or analyze sales data from HubSpot CRM",
            
            # Examples of what SHOULD trigger this
            positive_examples=[
                "Verificar dados de vendas",
                "Analisar os dados do HubSpot",
                "Conferir as vendas do CRM",
                "Check sales data accuracy",
                "Verify HubSpot data"
            ],
            
            # Examples of what should NOT trigger this
            negative_examples=[
                "What's the weather?",  # Weather trigger handles this
                "Search for something",  # Search trigger handles this
                "Hey bot",  # Assistant trigger handles this
                "Calculate something"  # Calculator handles this
            ]
        )
        
        # API configuration
        self.api_base_url = os.getenv("VERIFY_DATA_API_URL", "http://localhost:8000")
        self.hubspot_api_key = os.getenv("HUBSPOT_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
    
    def action(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Execute the data verification action
        
        Args:
            query: The user's spoken text
            **kwargs: Additional context (conversation history, etc.)
        
        Returns:
            Dict with 'text', 'speak', and optional 'voice_settings'
        """
        try:
            # Check if required API keys are configured
            if not self.hubspot_api_key or not self.openai_api_key:
                return {
                    "text": "Desculpe, as chaves da API não estão configuradas. Por favor, configure HUBSPOT_API_KEY e OPENAI_API_KEY no arquivo .env",
                    "speak": True
                }
            
            # Extract context from the query
            context = self._extract_context(query)
            
            # Prepare the prompt for data verification
            prompt = self._prepare_prompt(query)
            
            # Call the verify_data API
            response = self._call_verify_data_api(context, prompt)
            
            if response.get("error"):
                return {
                    "text": f"Erro ao verificar dados: {response['error']}",
                    "speak": True
                }
            
            # Format response for voice
            result_text = self._format_response(response.get("response", ""))
            
            return {
                "text": result_text,
                "speak": True,
                "voice_settings": {
                    "voice": "alloy",
                    "speed": 1.0
                }
            }
                
        except httpx.TimeoutException:
            return {
                "text": "A verificação de dados demorou muito para responder. Tente novamente.",
                "speak": True
            }
        except Exception as e:
            print(f"Verify data trigger error: {e}")
            return {
                "text": "Desculpe, houve um erro ao verificar os dados. Tente novamente.",
                "speak": True
            }
    
    def _extract_context(self, query: str) -> str:
        """Extract context from the user query"""
        # Simple context extraction - can be enhanced with NLP
        context_keywords = {
            "vendas": "Análise de dados de vendas",
            "deals": "Análise de negócios",
            "pipeline": "Análise de pipeline de vendas",
            "receita": "Análise de receita",
            "revenue": "Revenue analysis",
            "sales": "Sales analysis"
        }
        
        query_lower = query.lower()
        for keyword, context in context_keywords.items():
            if keyword in query_lower:
                return context
        
        return "Verificação geral de dados de vendas"
    
    def _prepare_prompt(self, query: str) -> str:
        """Prepare the prompt based on user query"""
        # Extract specific requests from the query
        if "incorreto" in query.lower() or "errado" in query.lower():
            return "Analise os dados e identifique possíveis inconsistências ou erros nos dados apresentados."
        elif "resumo" in query.lower() or "summary" in query.lower():
            return "Forneça um resumo dos dados de vendas atuais."
        elif "performance" in query.lower() or "desempenho" in query.lower():
            return "Analise a performance das vendas baseada nos dados do CRM."
        else:
            return f"Analise os dados de vendas e responda à seguinte pergunta: {query}"
    
    def _call_verify_data_api(self, context: str, prompt: str) -> Dict[str, Any]:
        """Call the verify_data API endpoint"""
        import asyncio
        
        async def make_request():
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "context": context,
                    "prompt": prompt
                }
                
                response = await client.post(
                    f"{self.api_base_url}/verify-data",
                    json=payload
                )
                
                return response.json()
        
        # Run async request in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(make_request())
            return result
        finally:
            loop.close()
    
    def _format_response(self, response: str) -> str:
        """Format API response for voice output"""
        # Keep response concise for voice
        # Remove excessive formatting and technical details
        
        # Limit response length for voice
        if len(response) > 500:
            # Take first 400 characters and add truncation message
            response = response[:400] + "... Para mais detalhes, acesse o dashboard."
        
        # Replace technical terms with voice-friendly versions
        response = response.replace("CRM", "sistema de vendas")
        response = response.replace("API", "sistema")
        response = response.replace("R$", "reais")
        
        return response 