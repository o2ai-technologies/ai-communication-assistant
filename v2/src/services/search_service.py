# src/services/search_service.py
from langchain_community.tools import TavilySearchResults

class SearchService:
    """A wrapper for the search tool."""
    def __init__(self, max_results: int = 5):
        self.search_tool = TavilySearchResults(max_results=max_results)

    def run(self, query: str) -> str:
        """Runs a search query and returns the results as a formatted string."""
        try:
            search_results = self.search_tool.run(query)
            # Format results consistently
            if isinstance(search_results, list):
                return "\n\n".join(
                    f"Title: {res.get('title', '')}\nContent: {res.get('content', '')}"
                    for res in search_results
                )
            return str(search_results)
        except Exception as e:
            print(f"Search Error: {e}")
            return "Не вдалося виконати пошук."