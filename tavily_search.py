import os
from tavily import TavilyClient

class TavilySearchClient:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        if not self.api_key or self.api_key == "your_tavily_api_key_here":
            self.client = None
        else:
            try:
                self.client = TavilyClient(api_key=self.api_key)
            except Exception:
                self.client = None

    def is_configured(self) -> bool:
        return self.client is not None

    def search(self, query: str) -> dict:
        """
        Searches the web using Tavily API.
        Returns a dictionary with 'context' string and 'sources' list.
        """
        if not self.is_configured():
            return {
                "context": "", 
                "sources": [], 
                "error": "Tavily API key is missing or invalid."
            }

        try:
            # We add keywords to favor authoritative sources if possible
            enhanced_query = f"{query} site:rbi.org.in OR bank"
            
            response = self.client.search(
                query=enhanced_query,
                search_depth="basic",
                max_results=3,
                include_answer=False
            )
            
            results = response.get("results", [])
            
            if not results:
                return {"context": "No relevant search results found.", "sources": []}
                
            context_parts = []
            sources = []
            
            for res in results:
                title = res.get('title', 'Unknown Title')
                url = res.get('url', '#')
                content = res.get('content', '')
                
                context_parts.append(f"Source: {title}\nURL: {url}\nContent: {content}")
                sources.append({"title": title, "url": url})
                
            return {
                "context": "\n\n".join(context_parts),
                "sources": sources
            }
            
        except Exception as e:
            return {
                "context": "", 
                "sources": [],
                "error": f"Search failed: {type(e).__name__}"
            }
