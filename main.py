from fastapi import FastAPI, File, HTTPException, UploadFile, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Dict
import ollama

from models_config import (
    LLM_SUMMARIZATION_MODEL,
    LLM_AUTOCOMPLETE_MODEL,
    LLM_CODE_GENERATION_MODEL,
    LLM_IMAGE_DESCRIPTION_MODEL,
    PROMPT_SUMMARIZE_TEXT,
    PROMPT_AUTOCOMPLETE_TEXT,
    PROMPT_DESCRIBE_IMAGE
)

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

@app.post("/summarize")
async def summarize_text(request: TextRequest) -> Dict[str, str]:
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    
    try:
        response = ollama.chat(model=LLM_SUMMARIZATION_MODEL, messages=[
            {
                'role': 'user',
                'content': f"{PROMPT_SUMMARIZE_TEXT}{request.text}",
            },
        ])
        summarized_text: str = response.get('message', {}).get('content', '')
        if not summarized_text:
            raise HTTPException(status_code=500, detail="Failed to generate a summary.")
        return {"summarized_text": summarized_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/autocomplete")
async def autocomplete_text(request: TextRequest) -> Dict[str, str]:
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    
    try:
        response = ollama.chat(model=LLM_AUTOCOMPLETE_MODEL, messages=[
            {
                'role': 'user',
                'content': f"{PROMPT_AUTOCOMPLETE_TEXT}{request.text}",
            },
        ])
        autocompleted_text: str = response.get('message', {}).get('content', '')
        if not autocompleted_text:
            raise HTTPException(status_code=500, detail="Failed to autocomplete text.")
        return {"autocompleted_text": autocompleted_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-code")
async def generate_code(request: TextRequest) -> Dict[str, str]:
    if not request.text:
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    
    try:
        result = ollama.generate(
            model=LLM_CODE_GENERATION_MODEL,
            prompt=request.text,
        )
        generated_code: str = result.get('response', '')
        if not generated_code:
            raise HTTPException(status_code=500, detail="Failed to generate code.")
        return {"generated_code": generated_code}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/describe-image")
async def describe_image(file: UploadFile = File(...)) -> Dict[str, str]:
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="Invalid image format. Only PNG, JPG, and JPEG are allowed.")
    
    image_path: str = "uploaded_image.jpg"
    try:
        image_data: bytes = await file.read()
        with open(image_path, "wb") as image_file:
            image_file.write(image_data)
        response = ollama.chat(
            model=LLM_IMAGE_DESCRIPTION_MODEL,
            messages=[
                {
                    'role': 'user',
                    'content': PROMPT_DESCRIBE_IMAGE,
                    'images': [image_path]
                }
            ]
        )
        description: str = response.get('message', {}).get('content', '')
        if not description:
            raise HTTPException(status_code=500, detail="Failed to describe the image.")
        return {"description": description.strip()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        import os
        if os.path.exists(image_path):
            os.remove(image_path)
