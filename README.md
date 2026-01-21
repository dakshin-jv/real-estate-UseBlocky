# Real Estate Chatbot API

A FastAPI-based chatbot that understands natural language queries and searches apartment listings.

## Setup

### Prerequisites
- Python 3.10+
- Ollama installed and running locally
- gpt-oss:20b model pulled in Ollama

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. Ensure Ollama is running:
```bash
ollama serve
```

4. Pull the model (if not already pulled):
```bash
ollama pull gpt-oss:20b
```

### Running the API

```bash
python -m src.app
```

The API will be available at `http://localhost:3000`

## API Endpoints

### POST /chat
Search for apartments using natural language.

**Request:**
```json
{
  "message": "Show me apartments under $1200 in New York"
}
```

**Response:**
```json
{
  "reply": "Found 2 apartments under $1200 in New York.",
  "results": [
    {
      "id": 1,
      "city": "New York",
      "bedrooms": 2,
      "price": 1100,
      "address": "123 Main St, Manhattan",
      "type": "apartment"
    },
    {
      "id": 3,
      "city": "New York",
      "bedrooms": 1,
      "price": 950,
      "address": "789 Broadway, Brooklyn",
      "type": "apartment"
    }
  ]
}
```

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

## Example Queries

- "Show me apartments under $1200 in New York"
- "Find 2 bedroom apartments in San Francisco"
- "What apartments are available in Los Angeles under $1500?"
- "Show me 1 bedroom apartments"
- "Find apartments in Chicago"

## Project Structure

```
src/
├── app.py           # FastAPI application
├── chatbot.py       # Core chatbot logic
├── models.py        # Pydantic models
└── data/
    └── properties.json  # Mock property data
```

## How It Works

1. User sends a natural language query to `/chat`
2. Ollama's gpt-oss:20b model parses the query using structured output (Pydantic schema)
3. Extracted filters (city, price, bedrooms) are used to search mock data
4. Matching properties are returned with a friendly reply

## Mock Data

The API includes 8 sample properties in `src/data/properties.json` across multiple cities:
- New York (3 properties)
- San Francisco (2 properties)
- Los Angeles (2 properties)
- Chicago (1 property)
