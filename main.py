from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import ollama  # Ensure you have the Ollama library installed and configured

app = FastAPI()

# Define the input schema for the summarization request
class SummarizationRequest(BaseModel):
    text: str  # Input text to summarize

# Define the input schema for the autocomplete request
class AutocompleteRequest(BaseModel):
    text: str  # Input text to autocomplete

@app.post("/summarize")
async def summarize_text(request: SummarizationRequest):
    try:
        # Using the Ollama library to interact with the model
        response = ollama.chat(model='llama3.1', messages=[
            {
                'role': 'user',
                'content': f"Summarize the following text: {request.text}",
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
async def autocomplete_text(request: AutocompleteRequest):
    try:
        # Using the Ollama library to interact with the model
        response = ollama.chat(model='tinyllama', messages=[
            {
                'role': 'user',
                'content': f"Autocomplete the following text: {request.text}",
            },
        ])

        # Extract the autocompleted text from the response
        autocompleted_text = response.get('message', {}).get('content', '')

        # Return the autocompleted text
        return {"autocompleted_text": autocompleted_text}
    
    except Exception as e:
        # If there's any error, raise an HTTP exception with status code 500
        raise HTTPException(status_code=500, detail=str(e))



# Run the server with: uvicorn main:app --reload
