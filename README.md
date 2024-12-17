# Translation API Server

[![Docker Build and Push](https://github.com/bmv234/Translate-API-Server/actions/workflows/docker-build.yml/badge.svg)](https://github.com/owner/Translate-API-Server/actions/workflows/docker-build.yml)

A simple REST API server that provides translation functionality using Argos Translate, with support for multiple languages and a web interface. Defaults to English to Spanish translation.

## Installation Options

You can install and run the server either locally or using Docker. Choose the method that best suits your needs.

### Local Installation

#### Requirements
- Python 3.12
- ~3GB disk space for all language models (downloads all available language pairs)

#### Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd Translation-API-Server
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Generate SSL certificates (required for HTTPS):
```bash
openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365 -subj '/CN=localhost'
```

### Docker Installation

#### Requirements
- Docker 24.0 or later
- ~4GB disk space (1GB for Docker image + 3GB for all language models)

#### Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd Translation-API-Server
```

2. Build the Docker image:
```bash
docker build -t translation-server .
```

This will:
- Install all dependencies
- Generate SSL certificates
- Set up health monitoring

## Running the Server

### Local Running

The server runs over HTTPS using self-signed certificates for security. After completing the local installation:

1. API-only version (recommended for production):
```bash
# Activate virtual environment if not already active
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Run API server
python main.py
```

2. Version with web interface (recommended for testing):
```bash
# Activate virtual environment if not already active
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows

# Run web interface server
python main-ui.py
```

Both versions will run on https://localhost:8000. When accessing the server:
- Your browser will show a security warning because of the self-signed certificate
- Click "Advanced" and "Proceed to localhost" to access the interface
- The web interface opens with English to Spanish translation by default
- The API-only version is more suitable for production deployments where only the REST API is needed

### Docker Running

After completing the Docker installation, you can run the server using either method:

1. Using docker-compose (recommended):
```bash
# Start the server
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the server
docker-compose down
```

2. Using docker command:
```bash
# Start the server
docker run -d --name translation-server \
  -p 8000:8000 \
  translation-server:latest

# View logs
docker logs -f translation-server

# Stop the server
docker stop translation-server
docker rm translation-server
```

### Verifying Installation

After starting the server, verify it's working:

1. Check the health endpoint:
```bash
curl --insecure https://localhost:8000/health
```

2. Test translation (defaults to English to Spanish):
```bash
curl --insecure -X POST "https://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello world", "from_lang": "en", "to_lang": "es"}'
```

3. Open web interface (if using main-ui.py):
   Visit https://localhost:8000 in your browser
   - You'll see a security warning due to the self-signed certificate
   - Click "Advanced" and "Proceed to localhost" to access the interface
   - The interface will open with English to Spanish translation ready to use

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: https://localhost:8000/docs
- ReDoc: https://localhost:8000/redoc

Note: When accessing the API documentation or making API calls:
- For development with self-signed certificates, use the `--insecure` flag with curl or disable certificate verification in your client
- For production, use properly signed SSL certificates from a trusted Certificate Authority

## Features

- Text translation using Argos Translate
- Default English to Spanish translation
- Support for multiple language pairs

### Supported Language Pairs

The server supports translation between the following languages:
- Arabic (ar) ↔ English (en)
- Chinese (zh) ↔ English (en)
- Dutch (nl) ↔ English (en)
- English (en) ↔ French (fr)
- English (en) ↔ German (de)
- English (en) ↔ Hindi (hi)
- English (en) ↔ Indonesian (id)
- English (en) ↔ Irish (ga)
- English (en) ↔ Italian (it)
- English (en) ↔ Japanese (ja)
- English (en) ↔ Korean (ko)
- English (en) ↔ Polish (pl)
- English (en) ↔ Portuguese (pt)
- English (en) ↔ Russian (ru)
- English (en) ↔ Spanish (es)
- English (en) ↔ Turkish (tr)
- English (en) ↔ Vietnamese (vi)
- French (fr) ↔ Spanish (es)
- Portuguese (pt) ↔ Spanish (es)

Note: The server automatically downloads models for all language pairs on first startup.
- Web interface for easy testing
- Language pair detection
- Comprehensive error handling
- Clean logging (warning suppression)
- CORS support for web applications
- Health check endpoint for monitoring

## Performance

- First-time startup will download all available language models (approximately 3GB, may take 10-15 minutes depending on your connection)
- Translation speed depends on text length and language pair
- Processing time is included in response headers as 'X-Process-Time'

## Error Handling

The API handles various error cases:
- 400: Invalid input (unsupported language pair)
- 500: Internal server error
- 503: Translation system not initialized

## Troubleshooting

### Common Installation Issues

1. SSL Certificate Issues:
   - Error: "SSL certificate verification failed"
   - Solution: Ensure SSL certificates are properly generated

2. Language Model Issues:
   - Error: "Language pair not available"
   - Solution: Check if the required language models are installed

### Common Runtime Issues

1. Port Conflicts:
   - Error: "Address already in use"
   - Solution: Stop other services using port 8000 or change the port:
     ```bash
     # Local
     PORT=8001 python main.py
     
     # Docker
     docker run -p 8001:8000 ...
     ```

2. Memory Issues:
   - Error: "Out of memory"
   - Solution: Reduce text size or free up system memory

## Notes

- The server uses Argos Translate for translation
- Defaults to English to Spanish translation
- Supports additional language pairs through downloadable models
- All API endpoints support CORS for web integration
- Models are cached for faster subsequent starts
- Warning messages are suppressed for cleaner logs