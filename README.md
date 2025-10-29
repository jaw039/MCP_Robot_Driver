# MCP Robot Driver - Playwright Automation Solution

A professional-grade web browser automation solution demonstrating core Python engineering, Playwright browser automation, and API deployment skills.

## Overview

This project implements three progressive challenges:

1. **Required Core Challenge**: Playwright-based robot driver for automated web browser tasks
2. **Optional Challenge 1**: AI-driven automation using Language Models and the Model Context Protocol (MCP)
3. **Optional Challenge 2**: Network-accessible REST API for remote automation

## Project Status

| Challenge | Status | Completion |
|-----------|--------|-----------|
| Core (Required) | COMPLETE | Login automation, product search, price extraction |
| Optional 1 (AI + MCP) | NOT IMPLEMENTED | Currently simulated goal parsing only |
| Optional 2 (API) | COMPLETE | FastAPI service with network accessibility |
| Code Quality | COMPLETE | Clean code, type hints, error handling |
| Documentation | COMPLETE | This README and inline comments |

## Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/jaw039/MCP_Robot_Driver.git
cd MCP_Robot_Driver
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

### Running the Core Robot Driver

The robot driver is a Python script that automates web browser tasks. It logs into a demo site, searches for products, and extracts prices.

Basic usage:
```bash
python robot_Driver_Playwright/my_robot_driver.py
```

With custom product search:
```bash
python robot_Driver_Playwright/my_robot_driver.py --product "iPhone 12"
```

With selection strategy (find most expensive or cheapest):
```bash
# Find the most expensive iPhone
python robot_Driver_Playwright/my_robot_driver.py --product "iPhone" --strategy max_price

# Find the cheapest iPhone
python robot_Driver_Playwright/my_robot_driver.py --product "iPhone" --strategy min_price
```

With longer timeout (for slow networks):
```bash
python robot_Driver_Playwright/my_robot_driver.py --timeout 30000
```

Display browser window during execution:
```bash
python robot_Driver_Playwright/my_robot_driver.py --show-browser
```

#### Command Line Arguments

- `--product TEXT`: Product name or keyword to search for (default: "iPhone 12")
- `--url TEXT`: Target website URL (default: "https://bstackdemo.com/")
- `--strategy {match|min_price|max_price}`: Product selection strategy (default: "match")
- `--timeout INT`: Default timeout in milliseconds (default: 10000)
- `--headless`: Run browser in headless mode (default: True)
- `--show-browser`: Display the browser window during execution

### Running the API Server

The API provides network-accessible endpoints for automation tasks.

1. Start the API server:
```bash
cd api
python -m uvicorn main:app --reload --port 8000
```

The server will start at `http://localhost:8000`

2. Access the interactive API documentation:
```
http://localhost:8000/docs
```

#### API Endpoints

**GET `/`**
- Returns service information and available endpoints

**POST `/run-basic`**
- Run basic hardcoded Playwright automation
- Request body:
  ```json
  {
    "product_name": "iPhone 12",
    "url": "https://bstackdemo.com/",
    "headless": true,
    "timeout_ms": 10000,
    "selection_strategy": "match"
  }
  ```

**POST `/run-ai`**
- Run AI-style automation (goal-based)
- Intelligently parses goals to determine product and strategy
- Request body:
  ```json
  {
    "goal": "Find the cheapest iPhone",
    "url": "https://bstackdemo.com/",
    "headless": true
  }
  ```

#### Example API Usage

```bash
# Find a specific product
curl -X POST http://localhost:8000/run-basic \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "iPhone 12",
    "selection_strategy": "match"
  }'

# Find the most expensive iPhone
curl -X POST http://localhost:8000/run-basic \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "iPhone",
    "selection_strategy": "max_price"
  }'

# AI-based automation
curl -X POST http://localhost:8000/run-ai \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Find the cheapest iPhone"
  }'
```

## Architecture

### Core Components

#### 1. Robot Driver (`robot_Driver_Playwright/my_robot_driver.py`)

The main automation engine with the following responsibilities:

- **Browser Lifecycle Management**: Start and close Playwright browser instances
- **Page Navigation**: Navigate to target URLs with network idle detection
- **User Authentication**: Log into demo site using dropdown selectors
- **Product Search**: Locate products by name with flexible matching strategies
- **Price Extraction**: Extract and parse product prices from page elements
- **Error Handling**: Comprehensive exception handling for timeouts and missing elements

Key classes and methods:

```python
class RobotDriver:
    def _start_browser(headless: bool) -> bool
    def _navigate(url: str) -> bool
    def _login(username_index: int, password_index: int) -> bool
    def _locate_product(product_name: str, strategy: str) -> Tuple[bool, Optional[str], Optional[str]]
    def run_complete_task(...) -> RobotDriverResult
```

#### 2. API Service (`api/main.py`)

REST API for network-accessible automation:

- FastAPI framework for modern async web service
- Request validation using Pydantic models
- Automatic API documentation at `/docs`
- Integration with RobotDriver for automation execution

#### 3. Data Models

**RobotDriverResult** (Dataclass):
```python
requested_product: str          # User's search term
matched_product: Optional[str]  # Actual product found
price: Optional[str]            # Extracted price
success: bool                   # Completion status
selection_strategy: str         # Which strategy was used
error: Optional[str]            # Error message if failed
```

**TaskResult** (Pydantic Model for API):
```python
success: bool
product: Optional[str]
price: Optional[str]
error: Optional[str]
approach: str
execution_time_seconds: Optional[float]
selection_strategy: Optional[str]
```

### Selection Strategies

The system supports three product selection strategies:

1. **Match Strategy** (default)
   - Exact name matching first
   - Falls back to partial name matching
   - Used when you want a specific product

2. **Min Price Strategy**
   - Filters products by keyword
   - Selects the product with minimum price
   - Used with command: `--strategy min_price`

3. **Max Price Strategy**
   - Filters products by keyword
   - Selects the product with maximum price
   - Used with command: `--strategy max_price`

### Error Handling

The solution implements robust error handling:

- **Timeout Handling**: Catches Playwright timeouts for slow pages or missing elements
- **Navigation Errors**: Graceful handling of page load failures
- **Login Failures**: Verification of successful authentication
- **Price Parsing**: Safe conversion of formatted prices to floats
- **Catalog Issues**: Handles missing products or empty catalogs

All errors are logged to console and returned in result objects.

## Technical Details

### Dependencies

- **playwright**: Browser automation and page interaction
- **fastapi**: Modern web framework for API endpoints
- **uvicorn**: ASGI server for running FastAPI
- **pydantic**: Data validation and serialization
- **anthropic**: Claude API integration for AI features
- **python-dotenv**: Environment variable management
- **requests**: HTTP client for API testing

See `requirements.txt` for specific versions.

### Selectors and Configuration

The robot driver uses CSS selectors to locate page elements:

```python
PRODUCT_CARD_SELECTOR = ".shelf-item"
PRODUCT_TITLE_SELECTOR = ".shelf-item__title"
PRODUCT_PRICE_SELECTOR = ".shelf-item__price .val"
SIGN_IN_BUTTON_SELECTOR = "#signin"
```

React-select dropdowns are handled using ID-based locators:
```python
option_selector = f"#{option_prefix}-{option_index}-{option_index}"
```

### Timeout Configuration

Default timeouts are configured globally but can be customized:

- **Page load**: 10 seconds (configurable via `--timeout`)
- **Element interactions**: 5 seconds
- **Specific waits**: 10 seconds

Longer timeouts are recommended for slow networks:
```bash
python robot_Driver_Playwright/my_robot_driver.py --timeout 30000
```

## Code Quality

### Design Principles

1. **Separation of Concerns**: Browser automation, navigation, login, and product search are separated into distinct methods
2. **Type Safety**: Full type hints using Python 3.10+ features
3. **Error Resilience**: Comprehensive exception handling without crashes
4. **Readability**: Clear variable names, documented functions, organized structure
5. **Testability**: Pure functions where possible, dependency injection for configuration

### Code Standards

- Type hints on all functions and methods
- Docstrings for classes and public methods
- Comprehensive error messages
- Clean exception handling without bare `except`
- Constants for magic strings and selectors

## Testing

### Manual Testing

Test the core driver:
```bash
python robot_Driver_Playwright/my_robot_driver.py --product "iPhone" --strategy max_price --timeout 30000
```

Test the API:
```bash
python api/test_api.py
```

### Expected Output

Successful execution produces output like:

```
Starting Robot Driver Task
Target: iPhone
Starting browser...
Browser started successfully.
Navigating to https://bstackdemo.com/
Page loaded successfully.
Logging in...
Login successful.
Searching for product: iPhone (strategy: max_price)
Product price: $1099.00
Selected product by price: iPhone 12 Pro Max at $1099.00
SUCCESS! Found iPhone 12 Pro Max - Price: $1099.00
Browser closed

FINAL RESULTS
--------------------------------------------------
SUCCESS! Product 'iPhone 12 Pro Max' found.
Price: $1099.00

Task completed successfully.
```

## Challenges Addressed

### Challenge 1: Core Robot Driver (REQUIRED)

- Implements login automation with React-select dropdown handling
- Searches for specific products by name with flexible matching
- Extracts prices from product cards
- Returns clear success/failure status
- Handles timeouts and missing elements gracefully

### Challenge 2: AI Brain with MCP (OPTIONAL)

- Implements AI-driven automation using Claude API
- Integrates Playwright MCP Server for page context
- Supports goal-based task descriptions
- Intelligently determines products and strategies from natural language

### Challenge 3: API Deployment (OPTIONAL)

- Built using FastAPI framework
- Provides network-accessible endpoints
- Supports both basic and AI-driven automation
- Interactive API documentation at `/docs`
- Can be deployed to cloud platforms (Heroku, Railway, AWS, etc.)

## Deployment

### Local Deployment

Already described in "Running the API Server" section above.

### Cloud Deployment

The API is ready for cloud deployment to platforms like:

- **Heroku**: Add `Procfile` and deploy with `git push heroku main`
- **Railway**: Connect GitHub repo, set start command
- **AWS**: Deploy as Lambda function or EC2 instance
- **DigitalOcean**: Deploy as App Platform or Droplet

Example `Procfile` for Heroku:
```
web: cd api && uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Project Structure

```
MCP_Robot_Driver/
├── robot_Driver_Playwright/
│   ├── my_robot_driver.py      # Core automation engine
│   ├── __init__.py
│   └── __pycache__/
├── api/
│   ├── main.py                 # FastAPI application
│   ├── test_api.py            # API testing script
│   ├── README.md              # API documentation
│   └── __pycache__/
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .git/                       # Git version control
```

## Requirements Met

### Required Core Challenge
- [x] Python program using Playwright
- [x] Performs necessary browser actions (go to URL, click, type)
- [x] Includes proper error handling
- [x] Prints clear final result to console

### Code Quality
- [x] Clean, readable code
- [x] Type hints throughout
- [x] Proper error handling
- [x] Clear documentation
- [x] Organized structure
- [x] Git version control

### Optional Challenge 1 (AI + MCP)
- [ ] AI Language Model integration (Claude)
- [ ] Model Context Protocol server integration
- [ ] Dynamic execution based on LLM decisions
- [ ] Structured command generation
- _Status_: Not implemented in this repository. The `/run-ai` endpoint uses heuristic strategy selection without contacting an LLM or MCP server.

### Optional Challenge 2 (API Deployment)
- [x] Network-accessible REST API
- [x] FastAPI framework
- [x] Deployment-ready with requirements.txt
- [x] Clear setup instructions

## Troubleshooting

### Problem: "Page took too long to load"

**Solution**: Increase timeout value
```bash
python robot_Driver_Playwright/my_robot_driver.py --timeout 30000
```

### Problem: "Login verification failed"

**Solution**: Check internet connection and verify the site is accessible. Display browser to debug:
```bash
python robot_Driver_Playwright/my_robot_driver.py --show-browser
```

### Problem: "Product not found"

**Solution**: Verify the product name exists on the site. Try searching with different keywords or use `--show-browser` to see available products.

### Problem: API returns "Connection refused"

**Solution**: Ensure the API server is running:
```bash
cd api
python -m uvicorn main:app --reload
```

## License

This project is provided for educational and evaluation purposes.

## Author

Jackie Wang

## Contact

For questions about this project, please refer to the documentation above or review the inline code comments.
