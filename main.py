from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import ollama  # Ensure you have the Ollama library installed and configured

app = FastAPI()

# Define the input schema for the summarization request
class SummarizationRequest(BaseModel):
    text: str  # Input text to summarize

@app.post("/summarize")
async def summarize_text(request: SummarizationRequest):
    try:
        # Using the Ollama library to interact with the model
        response = ollama.chat(model='tinyllama', messages=[
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

# Run the server with: uvicorn main:app --reload
