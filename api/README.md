# API Setup Instructions

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
playwright install chromium
```

2. **Set environment variables** (for AI automation):
```bash
# Create .env file in project root
echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here" > .env
```

3. **Start the API server:**
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access the API:**
- **Documentation:** http://localhost:8000/docs
- **Basic automation:** POST http://localhost:8000/run-basic
- **AI automation:** POST http://localhost:8000/run-ai

## API Endpoints

### 1. Basic Automation (Part 1)
**POST** `/run-basic`

Executes hardcoded Playwright automation.

**Request body:**
```json
{
  "url": "https://bstackdemo.com/",
  "product_name": "iPhone 12",
  "headless": true,
  "timeout_ms": 10000
}
```

**Response:**
```json
{
  "success": true,
  "product": "iPhone 12",
  "price": "$799.00",
  "error": null,
  "approach": "Basic Playwright automation",
  "execution_time_seconds": 15.23
}
```

### 2. AI-Driven Automation (Part 2)
**POST** `/run-ai`

Uses Claude AI with MCP for dynamic execution.

**Request body:**
```json
{
  "goal": "Find the cheapest iPhone and add it to cart",
  "url": "https://bstackdemo.com/",
  "headless": true,
  "max_iterations": 10
}
```

**Response:**
```json
{
  "success": true,
  "result": "Successfully found cheapest iPhone (XR $499) and added to cart",
  "error": null,
  "approach": "AI-driven MCP",
  "iterations_used": 4,
  "execution_time_seconds": 25.67
}
```

## Testing Examples

### Using curl:

**Basic automation:**
```bash
curl -X POST "http://localhost:8000/run-basic" \
  -H "Content-Type: application/json" \
  -d '{"product_name": "iPhone 12", "headless": true}'
```

**AI automation:**
```bash
curl -X POST "http://localhost:8000/run-ai" \
  -H "Content-Type: application/json" \
  -d '{"goal": "Find cheapest iPhone", "headless": true}'
```

### Using Python requests:

```python
import requests

# Basic automation
response = requests.post("http://localhost:8000/run-basic", json={
    "product_name": "iPhone 12",
    "headless": True
})
print(response.json())

# AI automation  
response = requests.post("http://localhost:8000/run-ai", json={
    "goal": "Find the cheapest iPhone and add it to cart",
    "headless": True
})
print(response.json())
```

## Features

- **Two automation approaches:** Basic (hardcoded) and AI-driven (MCP)
- **RESTful API:** Standard HTTP endpoints with JSON
- **Auto-documentation:** FastAPI generates interactive docs
- **Error handling:** Graceful failure with detailed error messages
- **Execution metrics:** Response time tracking
- **Flexible configuration:** Customizable timeouts, URLs, goals
- **Network accessible:** Run remotely via HTTP

## Deployment Ready

This API can be deployed to cloud platforms like:
- **Heroku:** `git push heroku main`
- **Railway:** Direct GitHub integration  
- **DigitalOcean App Platform:** Container deployment
- **AWS/GCP:** Container or serverless deployment