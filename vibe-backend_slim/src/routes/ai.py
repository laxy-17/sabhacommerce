from flask import Blueprint, request, jsonify
import logging
from src.ai_orchestrator import ai_orchestrator

ai_bp = Blueprint('ai', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@ai_bp.route('/generate-idea', methods=['POST'])
def generate_idea():
    """Generate a new idea using AI with optional research"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request body'}), 400
        
        prompt = data['prompt']
        
        # Use AI orchestrator for enhanced idea generation
        result = ai_orchestrator.generate_idea_with_research(prompt)
        
        logger.info(f"Generated idea for prompt: {prompt}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error generating idea: {str(e)}")
        return jsonify({'error': 'Failed to generate idea'}), 500

@ai_bp.route('/inspire', methods=['POST'])
def inspire():
    """Provide inspiration via web search and summarization"""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query in request body'}), 400
        
        query = data['query']
        
        # Use AI orchestrator for enhanced inspiration
        result = ai_orchestrator.inspire_with_search(query)
        
        logger.info(f"Generated inspiration for query: {query}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error generating inspiration: {str(e)}")
        return jsonify({'error': 'Failed to generate inspiration'}), 500

@ai_bp.route('/tools', methods=['GET'])
def get_tools():
    """Get available MCP tools"""
    try:
        tools = ai_orchestrator.get_tool_definitions()
        return jsonify({'tools': tools})
        
    except Exception as e:
        logger.error(f"Error retrieving tools: {str(e)}")
        return jsonify({'error': 'Failed to retrieve tools'}), 500

