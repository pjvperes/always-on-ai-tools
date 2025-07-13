# Verify Data Tool Integration Guide

## Overview

This document describes the integration of the `verify_data` tool into the voice assistant system. The tool analyzes sales data from HubSpot CRM using OpenAI for intelligent data verification and insights.

## Files Created/Modified

### 1. Core Integration Files

#### `verify_data.py` (Original API)
- FastAPI application with `/verify-data` endpoint
- Fetches HubSpot deals data
- Sends data to OpenAI for analysis
- Returns AI-generated insights

#### `triggers/builtin/verify_data_trigger.py`
- Proactive trigger for voice commands
- Keywords: "verificar dados", "verify data", "check data", "dados hubspot", etc.
- Calls the verify_data API endpoint
- Formats responses for voice output

#### `realtime/tools.py` (Modified)
- Added `verify_data_tool` function
- Integrates with Assistant Bot (Realtime API)
- Handles async API calls to verify_data endpoint

#### `realtime/session_manager.py` (Modified)
- Added tool schema for `verify_data_tool`
- Added handler method `_call_verify_data_tool`
- Integrated with existing tool system

### 2. Configuration Files

#### `config.py` (Modified)
- Added `verify_data_trigger` to enabled triggers
- Added `verify_data_tool` to enabled tools
- Set priority level 75 for the trigger

#### `main.py` (Modified)
- Added import for `VerifyDataTrigger`
- Added trigger loading in `load_triggers()` method

#### `config.example` (Modified)
- Added `VERIFY_DATA_API_URL` environment variable

## Environment Variables

Add these variables to your `.env` file:

```bash
# Data Verification API Configuration
VERIFY_DATA_API_URL=http://localhost:8000

# Required for the verify_data API
HUBSPOT_API_KEY=your_hubspot_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### 1. Proactive Trigger System

Activate by saying any of these keywords:
- "Verificar dados"
- "Verify data"
- "Check data"
- "Dados hubspot"
- "Conferir vendas"
- "Analisar dados"
- "Verificar vendas"
- "Check sales"
- "Dados do crm"
- "CRM data"
- "HubSpot data"
- "Sales data"

#### Example Voice Commands:
- "Verificar dados de vendas"
- "Analisar os dados do HubSpot"
- "Conferir as vendas do CRM"
- "Check sales data accuracy"

### 2. Assistant Bot Integration

During assistant mode conversations, the AI can automatically use the verify_data_tool when:
- User asks about sales data accuracy
- User wants to verify specific information
- User requests sales analysis

#### Example Assistant Interactions:
- User: "Hey Bot, can you verify our sales data?"
- User: "Check if the revenue numbers are correct"
- User: "Analyze the current sales pipeline"

## API Endpoints

### `/verify-data` (POST)
**Request Body:**
```json
{
  "context": "Sales data analysis",
  "prompt": "Analyze the sales data and identify any inconsistencies"
}
```

**Response:**
```json
{
  "response": "AI-generated analysis of the sales data..."
}
```

**Error Response:**
```json
{
  "error": "Error message describing what went wrong"
}
```

## Technical Details

### Trigger Priority
- **Priority**: 75 (High priority for data verification)
- **Execution**: Processes before weather (70) and search (60) triggers
- **Specificity**: Designed for sales data analysis keywords

### Tool Integration
- **Tool Name**: `verify_data_tool`
- **Parameters**: `context` (string) and `prompt` (string)
- **Timeout**: 30 seconds for API calls
- **Error Handling**: Comprehensive error handling with user-friendly messages

### Response Formatting
- **Voice Optimization**: Responses are formatted for voice output
- **Length Limitation**: Responses over 500 characters are truncated
- **Technical Term Replacement**: "CRM" → "sistema de vendas", "API" → "sistema"

## Testing

### 1. Test the API Directly
```bash
# Start the FastAPI application
python -m uvicorn verify_data:app --reload

# Test with curl
curl -X POST "http://localhost:8000/verify-data" \
  -H "Content-Type: application/json" \
  -d '{"context": "Sales analysis", "prompt": "Provide a summary of current sales data"}'
```

### 2. Test Proactive Trigger
```bash
# Start the voice assistant
python main.py

# Say one of the trigger keywords
# "Verificar dados de vendas"
```

### 3. Test Assistant Integration
```bash
# Start the voice assistant
python main.py

# Activate assistant mode
# "Hey Bot"

# Request data verification
# "Can you verify our sales data?"
```

## Error Handling

The integration includes comprehensive error handling:

1. **API Key Validation**: Checks for required HubSpot and OpenAI API keys
2. **Timeout Handling**: 30-second timeout for API calls
3. **Connection Errors**: Handles network connectivity issues
4. **API Response Errors**: Handles HTTP error responses
5. **Data Format Errors**: Handles malformed responses

## Troubleshooting

### Common Issues

1. **"API keys not configured"**
   - Solution: Add `HUBSPOT_API_KEY` and `OPENAI_API_KEY` to your `.env` file

2. **"Request timed out"**
   - Solution: Check network connectivity and API endpoint availability

3. **"Could not connect to the service"**
   - Solution: Ensure the verify_data API is running on the configured URL

4. **Trigger not activating**
   - Solution: Check that `verify_data_trigger` is in `enabled_triggers` in `config.py`

### Debug Mode

Enable debug logging by adding print statements in the trigger:

```python
def action(self, query: str, **kwargs) -> Dict[str, Any]:
    print(f"[DEBUG] Verify data trigger fired with query: '{query}'")
    # ... rest of the method
```

## Future Enhancements

1. **Enhanced Context Extraction**: Improve NLP for better parameter extraction
2. **Cache Integration**: Cache frequent queries for better performance
3. **Real-time Updates**: WebSocket integration for real-time data updates
4. **Multi-language Support**: Expand keyword support for other languages
5. **Advanced Analytics**: More sophisticated analysis options

## Security Considerations

1. **API Key Security**: Store API keys securely in environment variables
2. **Input Validation**: Validate all user inputs before processing
3. **Rate Limiting**: Implement rate limiting for API calls
4. **Data Privacy**: Ensure sensitive data is handled according to privacy requirements

## Dependencies

The integration uses these additional dependencies:
- `httpx`: For async HTTP requests
- `python-dotenv`: For environment variable management
- `asyncio`: For async operations

All dependencies are already included in `requirements.txt`. 