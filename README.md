# Zita API Deployment Guide

## Project Structure

```
zita-api/
├── main.py                 # FastAPI application entry point
├── pyproject.toml         # Poetry configuration and dependencies
├── render.yaml           # Render deployment configuration
├── Dockerfile           # Optional Docker configuration
├── .env.example        # Environment variables template
├── .gitignore         # Git ignore file
└── README.md         # This file
```

## Local Development Setup

### Prerequisites
- Python 3.8+
- Poetry (install from https://python-poetry.org/docs/#installation)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd zita-api
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env file with your actual API keys
   ```

4. **Run the application**
   ```bash
   poetry run uvicorn main:app --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## Deployment on Render

### Method 1: Using render.yaml (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New" → "Web Service"
   - Connect your GitHub repository

3. **Configure the service**
   - Render will automatically detect the `render.yaml` file
   - Set your environment variables in the Render dashboard:
     - `GROQ_API_KEY`: Your actual Groq API key

4. **Deploy**
   - Render will automatically build and deploy your application
   - You'll get a URL like `https://your-service-name.onrender.com`

### Method 2: Manual Configuration

If you prefer manual setup instead of using render.yaml:

1. **Create Web Service**
   - Service Name: `zita-api`
   - Environment: `Python 3`
   - Build Command: `pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev`
   - Start Command: `poetry run uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **Set Environment Variables**
   - Add `GROQ_API_KEY` with your actual API key

## Important Notes

### Before Deployment

1. **Add missing modules**: The current `main.py` has placeholder functions. You need to:
   - Add your `Zita/config.py` file with `BUSINESS_CATEGORIES`
   - Add your `utils/helpers.py` file with the actual implementation of:
     - `get_response()`
     - `process_function_call()`
     - `generate_business_description()`

2. **Update imports**: Uncomment and fix the import statements in `main.py`:
   ```python
   from Zita.config import BUSINESS_CATEGORIES
   from .utils.helpers import get_response, process_function_call, generate_business_description
   ```

3. **Test locally**: Make sure everything works locally before deploying

### Security Considerations

1. **CORS Configuration**: Update CORS settings for production:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],  # Specific domains
       allow_credentials=True,
       allow_methods=["GET", "POST", "DELETE"],
       allow_headers=["*"],
   )
   ```

2. **API Key Security**: Never commit API keys to git. Use environment variables.

3. **Rate Limiting**: Consider adding rate limiting for production use.

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `POST /chat/{session_id}` - Chat with the AI
- `POST /business-description` - Generate business description
- `GET /chat-history/{session_id}` - Get chat history
- `DELETE /chat-history/{session_id}` - Clear chat history
- `GET /business-categories` - Get available business categories
- `GET /function-call-log/{session_id}` - Get function call log
- `POST /create-session` - Create new chat session

## Environment Variables

- `GROQ_API_KEY` (required): Your Groq API key
- `PORT` (auto-set by Render): The port to run the server on
- `ENVIRONMENT` (optional): Set to "production" for production builds
- `DEBUG` (optional): Set to "false" for production
- `LOG_LEVEL` (optional): Set logging level

## Troubleshooting

### Common Issues

1. **Poetry not found**: Make sure Poetry is installed in the build command
2. **Import errors**: Ensure all your custom modules are included in the repository
3. **Environment variables**: Double-check that all required environment variables are set in Render
4. **Dependencies**: If you have additional dependencies, add them to `pyproject.toml`

### Logs

Check Render logs for deployment issues:
- Go to your service dashboard on Render
- Click on "Logs" tab to see build and runtime logs

## Scaling and Performance

- Render automatically handles basic scaling
- For high-traffic applications, consider:
  - Using a database for session storage instead of in-memory
  - Implementing proper caching
  - Adding monitoring and logging

## Support

For deployment issues:
- Check Render documentation: https://render.com/docs
- Check FastAPI documentation: https://fastapi.tiangolo.com/
- Check Poetry documentation: https://python-poetry.org/docs/