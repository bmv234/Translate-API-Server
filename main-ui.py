from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import logging
import os
import argostranslate.package
import argostranslate.translate
from pydantic import BaseModel

import warnings

# Filter out FutureWarnings
warnings.filterwarnings('ignore', category=FutureWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Translation Web Interface")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Initialize translation packages
@app.on_event("startup")
async def startup_event():
    """Initialize translation packages on startup"""
    try:
        logger.info("Downloading and installing translation packages...")
        argostranslate.package.update_package_index()
        available_packages = argostranslate.package.get_available_packages()
        
        # Download and install all available packages
        for package in available_packages:
            download_path = package.download()
            argostranslate.package.install_from_path(download_path)
        
        logger.info("Translation packages initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize translation packages: {str(e)}")
        raise RuntimeError("Failed to initialize translation system")

class TranslationRequest(BaseModel):
    text: str
    from_lang: str
    to_lang: str

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Render the web interface"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    """
    Translate text using Argos Translate
    """
    try:
        # Get available language pairs
        installed_languages = argostranslate.translate.get_installed_languages()
        from_lang = next((lang for lang in installed_languages if lang.code == request.from_lang), None)
        to_lang = next((lang for lang in installed_languages if lang.code == request.to_lang), None)

        if not from_lang or not to_lang:
            raise HTTPException(
                status_code=400,
                detail=f"Language pair {request.from_lang}->{request.to_lang} not available"
            )

        # Get translation for the language pair
        translation = from_lang.get_translation(to_lang)
        if not translation:
            raise HTTPException(
                status_code=400,
                detail=f"No translation available from {request.from_lang} to {request.to_lang}"
            )

        # Perform translation
        translated_text = translation.translate(request.text)
        
        return {
            "translated_text": translated_text,
            "from_lang": request.from_lang,
            "to_lang": request.to_lang,
            "original_text": request.text
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/languages")
async def get_available_languages():
    """Get list of available languages for translation"""
    try:
        installed_languages = argostranslate.translate.get_installed_languages()
        language_pairs = []
        
        # Get all possible language pairs
        for from_lang in installed_languages:
            for to_lang in installed_languages:
                if from_lang.code != to_lang.code:
                    translation = from_lang.get_translation(to_lang)
                    if translation:
                        language_pairs.append({
                            "from_lang": from_lang.code,
                            "from_name": from_lang.name,
                            "to_lang": to_lang.code,
                            "to_name": to_lang.name
                        })
        
        return {
            "available_languages": [
                {"code": lang.code, "name": lang.name}
                for lang in installed_languages
            ],
            "language_pairs": language_pairs
        }
    except Exception as e:
        logger.error(f"Error getting available languages: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        installed_languages = argostranslate.translate.get_installed_languages()
        return {
            "status": "healthy",
            "installed_languages": len(installed_languages),
            "language_pairs": sum(
                len(lang.get_translations())
                for lang in installed_languages
            )
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "detail": str(e)}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        ssl_keyfile="key.pem",
        ssl_certfile="cert.pem"
    )