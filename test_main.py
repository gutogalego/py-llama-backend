from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from io import BytesIO

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



# Test successful autocompletion
def test_autocomplete_text_success():
    payload = {"text": "This is a test text for autocompletion."}
    
    # Mock response from the Ollama model
    mock_response = {
        'message': {
            'content': 'This is a test text for autocompletion. Here is the completion.'
        }
    }
    
    with patch('ollama.chat', return_value=mock_response):
        response = client.post("/autocomplete", json=payload)
        assert response.status_code == 200
        assert response.json() == {"autocompleted_text": 'This is a test text for autocompletion. Here is the completion.'}

# Test with empty text input
def test_autocomplete_text_empty():
    payload = {"text": ""}
    
    response = client.post("/autocomplete", json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Text field cannot be empty.'}

# Test model failure scenario
def test_autocomplete_text_failure():
    payload = {"text": "This is a test text that should cause an error."}
    
    # Simulate a failure in the Ollama model
    with patch('ollama.chat', side_effect=Exception("Model failure")):
        response = client.post("/autocomplete", json=payload)
        assert response.status_code == 500
        assert response.json() == {"detail": "Model failure"}

# Test real autocompletion
def test_autocomplete_text_real():
    payload = {"text": "This is a test text for autocompletion."}

    # Send the request to the actual endpoint
    response = client.post("/autocomplete", json=payload)

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Extract the autocompleted text from the response
    response_data = response.json()

    # Perform assertions based on expected behavior
    # Here, we expect that the response will have an 'autocompleted_text' field
    assert 'autocompleted_text' in response_data


    # Test successful code generation
def test_generate_code_success():
    payload = {"text": "Generate a Python function to add two numbers."}
    
    # Mock response from the Ollama model
    mock_response = {
        'response': 'def add_numbers(a, b):\n    return a + b'
    }
    
    with patch('ollama.generate', return_value=mock_response):
        response = client.post("/generate-code", json=payload)
        assert response.status_code == 200
        assert response.json() == {"generated_code": 'def add_numbers(a, b):\n    return a + b'}

# Test with empty text input
def test_generate_code_empty():
    payload = {"text": ""}
    
    response = client.post("/generate-code", json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Text field cannot be empty.'}

# Test model failure scenario
def test_generate_code_failure():
    payload = {"text": "Generate a Python function to multiply two numbers."}
    
    # Simulate a failure in the Ollama model
    with patch('ollama.generate', side_effect=Exception("Model failure")):
        response = client.post("/generate-code", json=payload)
        assert response.status_code == 500
        assert response.json() == {"detail": "Model failure"}

# Test real code generation
def test_generate_code_real():
    payload = {"text": "Generate a Python function to reverse a string."}

    # Send the request to the actual endpoint
    response = client.post("/generate-code", json=payload)

    # Assert that the response status code is 200
    assert response.status_code == 200

    # Extract the generated code from the response
    response_data = response.json()

    # Perform assertions based on expected behavior
    # Here, we expect that the response will have a 'generated_code' field
    assert 'generated_code' in response_data

    # Test successful image description
def test_describe_image_success():
    # Create a mock image file
    image_file = BytesIO(b"mock image data")
    image_file.name = "test.png"
    
    # Mock response from the Ollama model
    mock_response = {
        'message': {
            'content': 'This is a chart describing the data.'
        }
    }
    
    with patch('ollama.chat', return_value=mock_response):
        response = client.post("/describe-image", files={"file": ("test.png", image_file, "image/png")})
        assert response.status_code == 200
        assert "chart" in response.json()["description"]

# Test with invalid image format
def test_describe_image_invalid_format():
    # Create a mock text file (not an image)
    text_file = BytesIO(b"mock text data")
    text_file.name = "test.txt"
    
    response = client.post("/describe-image", files={"file": ("test.txt", text_file, "text/plain")})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid image format. Only PNG, JPG, and JPEG are allowed.'}

# Test model failure scenario
def test_describe_image_failure():
    # Create a mock image file
    image_file = BytesIO(b"mock image data")
    image_file.name = "test.png"
    
    # Simulate a failure in the Ollama model
    with patch('ollama.chat', side_effect=Exception("Model failure")):
        response = client.post("/describe-image", files={"file": ("test.png", image_file, "image/png")})
        assert response.status_code == 500
        assert response.json() == {"detail": "Model failure"}

# Test real image description (requires an actual running service and valid model)
def test_describe_image_real():
    # Path to an actual image file to test with
    with open("test.png", "wb") as f:
        f.write(b"mock image data")  # Create a mock image file
    
    with open("test.png", "rb") as image_file:
        response = client.post("/describe-image", files={"file": ("test.png", image_file, "image/png")})
    
    assert response.status_code == 200
    response_data = response.json()
    assert 'description' in response_data
    assert "chart" in response_data["description"]