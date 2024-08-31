from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch

client = TestClient(app)

# Test successful summarization
def test_summarize_text_success():
    payload = {"text": "This is a test text to be summarized."}
    
    # Mock response from the Ollama model
    mock_response = {
        'message': {
            'content': 'This is a summarized version of the test text.'
        }
    }
    
    with patch('ollama.chat', return_value=mock_response):
        response = client.post("/summarize", json=payload)
        assert response.status_code == 200
        assert response.json() == {"summarized_text": 'This is a summarized version of the test text.'}

# Test with empty text input
def test_summarize_text_empty():
    payload = {"text": ""}
    
    response = client.post("/summarize", json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Text field cannot be empty.'}

# Test model failure scenario
def test_summarize_text_failure():
    payload = {"text": "This is a test text that should cause an error."}
    
    # Simulate a failure in the Ollama model
    with patch('ollama.chat', side_effect=Exception("Model failure")):
        response = client.post("/summarize", json=payload)
        assert response.status_code == 500
        assert response.json() == {"detail": "Model failure"}


def test_summarize_text_real():
    payload = {"text": "This is a test text to be summarized."}

    # Send the request to the actual endpoint
    response = client.post("/summarize", json=payload)

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Extract the summarized text from the response
    response_data = response.json()

    # Perform assertions based on expected behavior
    # Here, we expect that the response will have a 'summarized_text' field
    assert 'summarized_text' in response_data

