"""
AI Orchestrator
Integrates LLM with MCP tools for enhanced functionality
"""

import openai
import json
import logging
from typing import Dict, Any, List, Optional
from src.mcp_tools import mcp_tools

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """AI Orchestrator that combines LLM with MCP tools"""
    
    def __init__(self):
        self.client = openai.OpenAI()
        self.mcp_tools = mcp_tools
    
    def generate_idea_with_research(self, prompt: str) -> Dict[str, Any]:
        """
        Generate an idea using AI with optional web research
        
        Args:
            prompt: User's input prompt
            
        Returns:
            Generated idea with title, hook, and CTA
        """
        try:
            # First, determine if we need to do research
            research_prompt = f"""
            Analyze this prompt and determine if web research would be helpful: "{prompt}"
            
            Respond with JSON: {{"needs_research": true/false, "search_query": "query if needed"}}
            """
            
            research_response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": research_prompt}],
                max_tokens=100,
                temperature=0.3
            )
            
            try:
                research_decision = json.loads(research_response.choices[0].message.content)
            except:
                research_decision = {"needs_research": False}
            
            # Perform research if needed
            research_context = ""
            if research_decision.get("needs_research") and research_decision.get("search_query"):
                search_results = self.mcp_tools.web_search(research_decision["search_query"], 3)
                research_context = f"\n\nResearch context:\n{json.dumps(search_results, indent=2)}"
            
            # Generate the idea with research context
            idea_prompt = f"""
            Generate a creative and engaging idea based on this prompt: "{prompt}"
            {research_context}
            
            Return a JSON object with:
            - title: A catchy, engaging title
            - hook: A compelling description that draws people in
            - cta: A clear call-to-action
            
            Make it exciting and actionable!
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": idea_prompt}],
                max_tokens=300,
                temperature=0.8
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
            except:
                # Fallback if AI doesn't return valid JSON
                content = response.choices[0].message.content
                result = {
                    "title": "Creative Idea",
                    "hook": content[:150] + "..." if len(content) > 150 else content,
                    "cta": "Get Started"
                }
            
            logger.info(f"Generated idea with research for prompt: {prompt}")
            return result
            
        except Exception as e:
            logger.error(f"Error in AI orchestrator idea generation: {str(e)}")
            return {
                "title": "Inspiration Awaits",
                "hook": "Something amazing is waiting to be discovered. Let's explore new possibilities together!",
                "cta": "Discover More"
            }
    
    def inspire_with_search(self, query: str) -> Dict[str, Any]:
        """
        Provide inspiration using web search and AI summarization
        
        Args:
            query: The topic for inspiration
            
        Returns:
            Inspirational content with sources
        """
        try:
            # Perform web search
            search_results = self.mcp_tools.web_search(query, 5)
            
            # Create inspiration using search results
            inspiration_prompt = f"""
            Based on these search results about "{query}", create inspiring and motivational content:
            
            {json.dumps(search_results, indent=2)}
            
            Create content that:
            - Motivates and uplifts the reader
            - Provides actionable insights
            - Is positive and encouraging
            - References the search findings naturally
            
            Keep it engaging and inspiring!
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": inspiration_prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            inspiration_text = response.choices[0].message.content
            
            # Include source URLs from search results
            source_urls = [result.get("url") for result in search_results if result.get("url")]
            
            result = {
                "inspirationText": inspiration_text,
                "sourceUrl": source_urls[0] if source_urls else None,
                "additionalSources": source_urls[1:] if len(source_urls) > 1 else []
            }
            
            logger.info(f"Generated inspiration with search for query: {query}")
            return result
            
        except Exception as e:
            logger.error(f"Error in AI orchestrator inspiration: {str(e)}")
            return {
                "inspirationText": f"Every journey begins with a single step. Your interest in {query} shows you're ready to grow and explore new possibilities. Take that first step today!",
                "sourceUrl": None
            }
    
    def analyze_events_with_ai(self, events: List[Dict[str, Any]], user_preferences: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Analyze and enhance event data using AI
        
        Args:
            events: List of event data
            user_preferences: Optional user preferences for personalization
            
        Returns:
            Enhanced events with AI-generated insights
        """
        try:
            if not events:
                return events
            
            # Create AI prompt for event analysis
            analysis_prompt = f"""
            Analyze these events and add helpful insights for each:
            
            {json.dumps(events, indent=2)}
            
            For each event, add:
            - aiInsight: A brief, helpful insight about why this event might be interesting
            - personalityMatch: What type of person would enjoy this event
            - preparationTips: 1-2 quick tips for attending
            
            Return the events array with these new fields added.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": analysis_prompt}],
                max_tokens=800,
                temperature=0.6
            )
            
            try:
                enhanced_events = json.loads(response.choices[0].message.content)
                if isinstance(enhanced_events, list):
                    logger.info(f"Enhanced {len(enhanced_events)} events with AI insights")
                    return enhanced_events
            except:
                pass
            
            # Fallback: return original events
            return events
            
        except Exception as e:
            logger.error(f"Error in AI event analysis: {str(e)}")
            return events
    
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get available MCP tool definitions"""
        return self.mcp_tools.get_available_tools()

# Global AI orchestrator instance
ai_orchestrator = AIOrchestrator()

