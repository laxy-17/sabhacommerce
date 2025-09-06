"""
MCP (Model Context Protocol) Tooling
Provides wrappers for http.getJSON, web.search, db.query
Exposes these as tools available to the AI orchestrator
"""

import requests
import json
import logging
from typing import Dict, Any, List, Optional
import sqlite3
import os

logger = logging.getLogger(__name__)

class MCPTools:
    """MCP Tools wrapper class"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    
    def http_get_json(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        HTTP GET request that returns JSON data
        
        Args:
            url: The URL to make the request to
            headers: Optional headers to include in the request
            
        Returns:
            Dict containing the JSON response
        """
        try:
            response = requests.get(url, headers=headers or {}, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP GET request failed: {str(e)}")
            return {"error": f"HTTP request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON response: {str(e)}")
            return {"error": f"Invalid JSON response: {str(e)}"}
    
    def web_search(self, query: str, num_results: int = 5) -> List[Dict[str, Any]]:
        """
        Web search functionality (mock implementation)
        In production, this would integrate with search APIs like Google Custom Search
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of search result dictionaries
        """
        # Mock search results for demonstration
        # In production, integrate with actual search APIs
        mock_results = [
            {
                "title": f"Search result for '{query}' - Article 1",
                "url": f"https://example.com/article1?q={query}",
                "snippet": f"This is a relevant article about {query} that provides useful information...",
                "source": "example.com"
            },
            {
                "title": f"Search result for '{query}' - Guide",
                "url": f"https://guide.com/topic?search={query}",
                "snippet": f"A comprehensive guide covering {query} with step-by-step instructions...",
                "source": "guide.com"
            },
            {
                "title": f"Search result for '{query}' - News",
                "url": f"https://news.com/latest?topic={query}",
                "snippet": f"Latest news and updates related to {query} from reliable sources...",
                "source": "news.com"
            }
        ]
        
        logger.info(f"Web search performed for query: {query}")
        return mock_results[:num_results]
    
    def db_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Database query execution
        
        Args:
            query: SQL query string
            params: Optional query parameters
            
        Returns:
            List of query result dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            cursor.execute(query, params or ())
            results = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            logger.info(f"Database query executed successfully: {query}")
            return results
            
        except sqlite3.Error as e:
            logger.error(f"Database query failed: {str(e)}")
            return [{"error": f"Database query failed: {str(e)}"}]
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Returns a list of available MCP tools for the AI orchestrator
        
        Returns:
            List of tool definitions
        """
        return [
            {
                "name": "http_get_json",
                "description": "Make HTTP GET requests and return JSON data",
                "parameters": {
                    "url": {"type": "string", "required": True, "description": "URL to make the request to"},
                    "headers": {"type": "object", "required": False, "description": "Optional headers"}
                }
            },
            {
                "name": "web_search",
                "description": "Search the web for information",
                "parameters": {
                    "query": {"type": "string", "required": True, "description": "Search query"},
                    "num_results": {"type": "integer", "required": False, "description": "Number of results to return (default: 5)"}
                }
            },
            {
                "name": "db_query",
                "description": "Execute database queries",
                "parameters": {
                    "query": {"type": "string", "required": True, "description": "SQL query to execute"},
                    "params": {"type": "array", "required": False, "description": "Query parameters"}
                }
            }
        ]
    
    def execute_tool(self, tool_name: str, **kwargs) -> Any:
        """
        Execute a specific MCP tool by name
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool-specific arguments
            
        Returns:
            Tool execution result
        """
        if tool_name == "http_get_json":
            return self.http_get_json(kwargs.get("url"), kwargs.get("headers"))
        elif tool_name == "web_search":
            return self.web_search(kwargs.get("query"), kwargs.get("num_results", 5))
        elif tool_name == "db_query":
            return self.db_query(kwargs.get("query"), kwargs.get("params"))
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

# Global MCP tools instance
mcp_tools = MCPTools()

