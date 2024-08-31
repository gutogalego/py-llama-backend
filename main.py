# main.py
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
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

@app.post("/summarize")
async def summarize_text(request: TextRequest) -> Dict[str, str]:
    """
    Endpoint to summarize the provided text using the specified LLM model.
    
    Args:
    - request: TextRequest containing the text to be summarized.

    Returns:
    - A dictionary with the summarized text.
    """
    try:
        response = ollama.chat(model=LLM_SUMMARIZATION_MODEL, messages=[
            {
                'role': 'user',
                'content': f"{PROMPT_SUMMARIZE_TEXT}{request.text}",
            },
        ])
        summarized_text: str = response.get('message', {}).get('content', '')
        return {"summarized_text": summarized_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/autocomplete")
async def autocomplete_text(request: TextRequest) -> Dict[str, str]:
    """
    Endpoint to autocomplete the provided text using the specified LLM model.

    Args:
    - request: TextRequest containing the text to autocomplete.

    Returns:
    - A dictionary with the autocompleted text.
    """
    try:
        response = ollama.chat(model=LLM_AUTOCOMPLETE_MODEL, messages=[
            {
                'role': 'user',
                'content': f"{PROMPT_AUTOCOMPLETE_TEXT}{request.text}",
            },
        ])
        autocompleted_text: str = response.get('message', {}).get('content', '')
        return {"autocompleted_text": autocompleted_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-code")
async def generate_code(request: TextRequest) -> Dict[str, str]:
    """
    Endpoint to generate code based on the provided text prompt using the specified LLM model.

    Args:
    - request: TextRequest containing the prompt text for code generation.

    Returns:
    - A dictionary with the generated code.
    """
    try:
        result = ollama.generate(
            model=LLM_CODE_GENERATION_MODEL,
            prompt=request.text,
        )
        return {"generated_code": result['response']}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/describe-image")
async def describe_image(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    Endpoint to describe the uploaded image using the specified LLM model.

    Args:
    - file: UploadFile object containing the image to describe.

    Returns:
    - A dictionary with the image description.
    """
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
        return {"description": description.strip()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        import os
        if os.path.exists(image_path):
            os.remove(image_path)
