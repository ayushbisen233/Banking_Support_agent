from gemini_client import GeminiClient
from tavily_search import TavilySearchClient
from prompts import SYSTEM_PROMPT, INTENT_DETECTION_PROMPT
from banking_data import get_customer_summary

class BankingAgent:
    def __init__(self):
        self.gemini = GeminiClient()
        self.tavily = TavilySearchClient()

    def process_query(self, query: str) -> dict:
        """
        Processes a user query through the agent pipeline:
        1. Intent detection
        2. Web search (if needed)
        3. Response generation
        """
        if not query or not query.strip():
            return {
                "response": "Please ask a question.",
                "intent": "None",
                "search_required": False,
                "sources": [],
                "activity_log": ["✓ Query received: Empty"]
            }

        activity_log = ["✓ Query received"]
        
        # 1. Detect Intent
        intent_data = self.gemini.detect_intent(query, INTENT_DETECTION_PROMPT)
        
        if "error" in intent_data:
            return {
                "response": f"System Error: {intent_data['error']}",
                "intent": "ERROR",
                "search_required": False,
                "sources": [],
                "activity_log": activity_log + ["✗ Intent detection failed"]
            }
            
        intent = intent_data.get("intent", "GENERAL")
        requires_search = intent_data.get("requires_search", False)
        
        activity_log.append(f"✓ Intent detected: {intent.replace('_', ' ').title()}")
        activity_log.append(f"✓ Web search required: {'Yes' if requires_search else 'No'}")
        
        # 2. Gather Context
        context_parts = []
        sources = []
        
        # Add mock banking data if relevant to account/card
        if intent in ["ACCOUNT", "CARD", "TRANSACTION", "LOAN"]:
            context_parts.append(f"Mock Customer Data:\n{get_customer_summary()}")
            activity_log.append("✓ Mock customer data loaded")
            
        # Perform Web Search if required
        if requires_search:
            search_result = self.tavily.search(query)
            if "error" in search_result:
                context_parts.append(f"[Search Failed: {search_result['error']}. Inform the user that current information could not be verified.]")
                activity_log.append("✗ Tavily search failed")
            else:
                context_parts.append(f"Search Results:\n{search_result['context']}")
                sources = search_result['sources']
                activity_log.append("✓ Tavily search completed")
                
        # 3. Generate Final Response
        final_context = "\n\n".join(context_parts)
        
        response = self.gemini.generate_response(
            system_prompt=SYSTEM_PROMPT,
            user_query=query,
            context=final_context
        )
        
        activity_log.append("✓ Gemini response generated")
        
        return {
            "response": response,
            "intent": intent,
            "search_required": requires_search,
            "sources": sources,
            "activity_log": activity_log
        }
