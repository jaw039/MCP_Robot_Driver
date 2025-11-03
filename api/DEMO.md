# Challenge 2 Demo: Network-Accessible Robot Driver

## What This Demonstrates

- Web access: FastAPI creates browser-triggerable endpoints  
- Launch links: Specific routes start automation remotely  
- Easy setup: Clear instructions plus `requirements.txt`  
- Network service: Core program exposed as an API  

## How to Run the Demo

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Start the API Server
```bash
cd api
./start_server.sh
# OR manually: uvicorn main:app --reload --port 8000
```

### Step 3: Test the API

**Option A: Use the interactive docs**
- Open: http://localhost:8000/docs
- Try the endpoints directly in browser

**Option B: Use curl commands**
```bash
# Basic automation
curl -X POST "http://localhost:8000/run-basic" \
  -H "Content-Type: application/json" \
  -d '{"product_name": "iPhone 12", "headless": true}'

# AI-style automation  
curl -X POST "http://localhost:8000/run-ai" \
  -H "Content-Type: application/json" \
  -d '{"goal": "Find the cheapest iPhone", "headless": true}'
```

**Option C: Use the test script**
```bash
python api/test_api.py
```

## API Endpoints Created

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | API info and available endpoints |
| `/run-basic` | POST | Execute hardcoded automation |
| `/run-ai` | POST | Execute AI-guided automation |
| `/docs` | GET | Interactive API documentation |

## Example API Calls

### Basic Automation Request
```json
POST /run-basic
{
  "url": "https://bstackdemo.com/",
  "product_name": "iPhone 12", 
  "headless": true,
  "timeout_ms": 10000
}
```

### Response
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

## Challenge 2 Requirements Met

- Goal: Turn core program into a network-accessible service  
- Web access: FastAPI provides HTTP endpoints  
- Launch links: `/run-basic` and `/run-ai` endpoints  
- Easy setup: `requirements.txt` plus clear instructions  
- Remote automation: Send HTTP requests to trigger browser automation  

## Deployment Ready

This API can be deployed to cloud platforms:

**Heroku:**
```bash
# Add Procfile: web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
git push heroku main
```

**Railway:**
```bash
# Connect GitHub repo, auto-deploys
```

**DigitalOcean/AWS:**
```bash
# Container deployment with Dockerfile
```

The API is production-ready with error handling, documentation, and standard REST patterns.