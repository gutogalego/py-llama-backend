# main.py
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
import ollama  # Ensure you have the Ollama library installed and configured

# Import models and prompts from models_config.py
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

# Define the input schema for the summarization request
class TextRequest(BaseModel):
    text: str  # Input text to summarize


@app.post("/summarize")
async def summarize_text(request: TextRequest):
    try:
        # Using the Ollama library to interact with the model
        response = ollama.chat(model=LLM_SUMMARIZATION_MODEL, messages=[
            {
                'role': 'user',
                'content': f"{PROMPT_SUMMARIZE_TEXT}{request.text}",
            },
        ])

        # Extract the summarized content from the response
        summarized_text = response.get('message', {}).get('content', '')

        # Return the summarized text
        return {"summarized_text": summarized_text}
    
    except Exception as e:
        # If there's any error, raise an HTTP exception with status code 500
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/autocomplete")
async def autocomplete_text(request: TextRequest):
    try:
        # Using the Ollama library to interact with the model
        response = ollama.chat(model=LLM_AUTOCOMPLETE_MODEL, messages=[
            {
                'role': 'user',
                'content': f"{PROMPT_AUTOCOMPLETE_TEXT}{request.text}",
            },
        ])

        # Extract the autocompleted text from the response
        autocompleted_text = response.get('message', {}).get('content', '')

        # Return the autocompleted text
        return {"autocompleted_text": autocompleted_text}
    
    except Exception as e:
        # If there's any error, raise an HTTP exception with status code 500
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-code")
async def generate_code(request: TextRequest):
    try:
        # Using the Ollama library to generate code
        result = ollama.generate(
            model=LLM_CODE_GENERATION_MODEL,
            prompt=request.text,
        )

        # Return the generated code
        return {"generated_code": result['response']}
    
    except Exception as e:
        # If there's any error, raise an HTTP exception with status code 500
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/describe-image")
async def describe_image(file: UploadFile = File(...)):
    try:
        # Read the image file from the request
        image_data = await file.read()

        # Save the uploaded image to a temporary location (if needed)
        with open("uploaded_image.jpg", "wb") as image_file:
            image_file.write(image_data)

        # Using Ollama's model to interact with the image
        response = ollama.chat(
            model=LLM_IMAGE_DESCRIPTION_MODEL,
            messages=[
                {
                    'role': 'user',
                    'content': PROMPT_DESCRIBE_IMAGE,
                    'images': ['./uploaded_image.jpg']  # Point to the saved image file
                }
            ]
        )

        # Extract the description from the response
        description = response.get('message', {}).get('content', '')

        # Return the description
        return {"description": description.strip()}
    
    except Exception as e:
        # If there's any error, raise an HTTP exception with status code 500
        raise HTTPException(status_code=500, detail=str(e))
