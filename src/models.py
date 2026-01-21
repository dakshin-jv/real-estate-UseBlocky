from pydantic import BaseModel, Field
from typing import Optional, List


class PropertyFilter(BaseModel):
    """Extracted filters from user query"""
    city: Optional[str] = Field(None, description="City name")
    max_price: Optional[int] = Field(None, description="Maximum price")
    min_bedrooms: Optional[int] = Field(None, description="Minimum bedrooms")
    max_bedrooms: Optional[int] = Field(None, description="Maximum bedrooms")


class QueryParsing(BaseModel):
    """Parsed user query with extracted entities"""
    intent: str = Field(description="Intent: search_property or other")
    filters: PropertyFilter = Field(description="Extracted filters")
    message: Optional[str] = Field(None, description="Message for non-search intents")


class Property(BaseModel):
    """Property listing"""
    id: int
    city: str
    bedrooms: int
    price: int
    address: str
    type: str


class ChatRequest(BaseModel):
    """Chat API request"""
    message: str = Field(description="User query")


class ChatResponse(BaseModel):
    """Chat API response"""
    reply: str = Field(description="Assistant reply")
    results: List[Property] = Field(description="Matching properties")
