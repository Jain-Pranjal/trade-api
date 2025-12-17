# Trade API - Indian Market Sector Analysis

A FastAPI-based REST API that provides AI-powered market analysis for Indian sectors using Google Gemini AI.

## Features

- AI-powered sector analysis using Google Gemini
- Real-time market news integration
- Automated markdown report generation
- JWT authentication
- Rate limiting (configurable)
- Pydantic-based configuration management
- Session tracking by IP
- Input validation for allowed sectors

## Supported Sectors (configurable)

- Pharmaceuticals
- Technology
- Agriculture
- Finance
- Energy
- Healthcare
- Real Estate
- Consumer Goods
- Utilities
- Telecommunications

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key

## Installation

### 1. Install uv (if not already installed)

**macOS/Linux:**

```bash
brew install uv
```

Or using curl:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**

```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone the repository

```bash
git clone https://github.com/Jain-Pranjal/trade-api.git
```

### 3. Sync dependencies

```bash
uv sync
```

This will create a virtual environment and install all required dependencies.

### 4. Set up environment variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (defaults provided)
JWT_SECRET=super-secret-change-in-production
RATE_LIMIT=5
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=development
```

## Running the Application

Start the server:

```bash
uv run ./main.py
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### 1. Simple Check

```bash
GET /
```

### 2. Generate JWT Token

```bash
POST /auth/token?username=your_username
```

### 3. Analyze Sector (Protected)

```bash
GET /analyze/{sector}
Headers: Authorization: Bearer <your_jwt_token>
```

Example:

```bash
curl -X GET "http://localhost:8000/analyze/technology" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Example Response

```json
{
  "sector": "technology",
  "report": "# Technology Sector Market Analysis...",
  "saved_to": "/path/to/reports/technology_20251218_143025.md",
  "message": "Report saved successfully",
  "session": {
    "request_count": 1,
    "first_active": "2025-12-18T14:30:25",
    "last_active": "2025-12-18T14:30:25"
  }
}
```

## Project Structure

```
trade api/
├── config.py              # Pydantic settings configuration
├── main.py                # Application entry point
├── server.py              # FastAPI app and routes
├── pyproject.toml         # Project dependencies
├── .env                   # Environment variables (create this)
├── models/
│   └── schema.py          # Pydantic models for validation
├── services/
│   ├── ai_service.py      # Gemini AI integration
│   ├── markdown_report.py # Report generation
│   └── trade_search.py    # Market news fetching
├── security/
│   ├── auth.py            # JWT authentication
│   ├── jwt.py             # JWT token utilities
│   └── rate_limit.py      # Rate limiting setup
├── utils/
│   └── session.py         # Session tracking
└── reports/               # Generated reports (auto-created)
```

## Configuration

All configuration is managed through Pydantic Settings in [config.py](config.py). Settings can be overridden using environment variables or a `.env` file.

See [.env.example](.env.example) for all available configuration options.

## Development

To run in development mode with auto-reload:

```bash
uv run ./main.py
```

The server will automatically reload when you make changes to the code.

## Error Handling

The API provides clean JSON error responses for:

- Invalid sector input (400)
- Authentication errors (401)
- Rate limit exceeded (429)
- AI service errors (503)
- Validation errors (422)

## Notes

- Reports are saved locally in the `reports/` directory
- Session tracking is in-memory (resets on server restart)
- Rate limiting is IP-based
- JWT tokens expire after 30 minutes (configurable)

## License

[MIT License](LICENSE)
