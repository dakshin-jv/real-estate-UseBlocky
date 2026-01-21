import json
import os
from typing import List
from ollama import chat
from src.models import QueryParsing, Property, PropertyFilter
from src.prompts import QUERY_PARSING_SYSTEM_PROMPT, REPLY_GENERATION_SYSTEM_PROMPT

# Load properties
data_path = os.path.join(os.path.dirname(__file__), 'data', 'properties.json')
with open(data_path) as f:
    properties = [Property(**p) for p in json.load(f)]


def parse_user_query(message: str) -> QueryParsing:
    """Extract intent and filters from user message."""
    response = chat(
        model='llama3.2:latest',
        messages=[
            {'role': 'system', 'content': QUERY_PARSING_SYSTEM_PROMPT},
            {'role': 'user', 'content': message}
        ],
        format=QueryParsing.model_json_schema(),
    )
    return QueryParsing.model_validate_json(response.message.content)


def filter_properties(filters: PropertyFilter) -> List[Property]:
    """Filter properties based on criteria."""
    results = properties
    if filters.city:
        results = [p for p in results if p.city.lower() == filters.city.lower()]
    if filters.max_price:
        results = [p for p in results if p.price <= filters.max_price]
    if filters.min_bedrooms:
        results = [p for p in results if p.bedrooms >= filters.min_bedrooms]
    if filters.max_bedrooms:
        results = [p for p in results if p.bedrooms <= filters.max_bedrooms]
    return results


def generate_reply(message: str, results: List[Property], filters: PropertyFilter) -> str:
    """Generate reply using LLM."""
    try:
        filters_dict = {k: v for k, v in filters.dict().items() if v is not None}
        
        if not filters_dict:
            return "No results found."
        
        results_list = [r.dict() for r in results]
        
        prompt = f"""User Query: {message}
Filters: {filters_dict}
Results: {results_list}"""
        
        response = chat(
            model='llama3.2:latest',
            messages=[
                {'role': 'system', 'content': REPLY_GENERATION_SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt}
            ],
        )
        return response.message.content.strip()
    except Exception as e:
        print(f"Error generating reply: {e}")
        return "No results found."


def chat_with_properties(message: str) -> tuple[str, List[Property]]:
    """Process user message and return reply with results."""
    try:
        parsed = parse_user_query(message)
        
        if parsed.intent == "other":
            return parsed.message or "I help with apartment searches.", []
        
        results = filter_properties(parsed.filters)
        reply = generate_reply(message, results, parsed.filters)
        
        return reply, results
    except Exception as e:
        print(f"Error: {e}")
        return "Unable to process request.", []
