from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from io import BytesIO


client = TestClient(app)

def test_summarize_text_success():
    payload = {"text": "This is a test text to be summarized."}
    mock_response = {
        'message': {
            'content': 'This is a summarized version of the test text.'
        }
    }
    with patch('ollama.chat', return_value=mock_response):
        response = client.post("/summarize", json=payload)
        assert response.status_code == 200
        assert response.json() == {"summarized_text": 'This is a summarized version of the test text.'}

def test_summarize_text_empty():
    payload = {"text": ""}
    response = client.post("/summarize", json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Text field cannot be empty.'}

def test_summarize_text_failure():
    payload = {"text": "This is a test text that should cause an error."}
    with patch('ollama.chat', side_effect=Exception("Model failure")):
        response = client.post("/summarize", json=payload)
        assert response.status_code == 500
        assert response.json() == {"detail": "Model failure"}

def test_summarize_text_real():
    payload = {"text": "This is a test text to be summarized."}
    response = client.post("/summarize", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert 'summarized_text' in response_data

def test_autocomplete_text_success():
    payload = {"text": "This is a test text for autocompletion."}
    mock_response = {
        'message': {
            'content': 'This is a test text for autocompletion. Here is the completion.'
        }
    }
    with patch('ollama.chat', return_value=mock_response):
        response = client.post("/autocomplete", json=payload)
        assert response.status_code == 200
        assert response.json() == {"autocompleted_text": 'This is a test text for autocompletion. Here is the completion.'}

def test_autocomplete_text_empty():
    payload = {"text": ""}
    response = client.post("/autocomplete", json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Text field cannot be empty.'}

def test_autocomplete_text_failure():
    payload = {"text": "This is a test text that should cause an error."}
    with patch('ollama.chat', side_effect=Exception("Model failure")):
        response = client.post("/autocomplete", json=payload)
        assert response.status_code == 500
        assert response.json() == {"detail": "Model failure"}

def test_autocomplete_text_real():
    payload = {"text": "This is a test text for autocompletion."}
    response = client.post("/autocomplete", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert 'autocompleted_text' in response_data

def test_generate_code_success():
    payload = {"text": "Generate a Python function to add two numbers."}
    mock_response = {
        'response': 'def add_numbers(a, b):\n    return a + b'
    }
    with patch('ollama.generate', return_value=mock_response):
        response = client.post("/generate-code", json=payload)
        assert response.status_code == 200
        assert response.json() == {"generated_code": 'def add_numbers(a, b):\n    return a + b'}

def test_generate_code_empty():
    payload = {"text": ""}
    response = client.post("/generate-code", json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Text field cannot be empty.'}

def test_generate_code_failure():
    payload = {"text": "Generate a Python function to multiply two numbers."}
    with patch('ollama.generate', side_effect=Exception("Model failure")):
        response = client.post("/generate-code", json=payload)
        assert response.status_code == 500
        assert response.json() == {"detail": "Model failure"}

def test_generate_code_real():
    payload = {"text": "Generate a Python function to reverse a string."}
    response = client.post("/generate-code", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert 'generated_code' in response_data

def test_describe_image_success():
    image_file = BytesIO(b"mock image data")
    image_file.name = "test.png"
    mock_response = {
        'message': {
            'content': 'This is a chart describing the data.'
        }
    }
    with patch('ollama.chat', return_value=mock_response):
        response = client.post("/describe-image", files={"file": ("test.png", image_file, "image/png")})
        assert response.status_code == 200
        assert "chart" in response.json()["description"]

def test_describe_image_invalid_format():
    text_file = BytesIO(b"mock text data")
    text_file.name = "test.txt"
    response = client.post("/describe-image", files={"file": ("test.txt", text_file, "text/plain")})
    assert response.status_code == 400
    assert response.json() == {'detail': 'Invalid image format. Only PNG, JPG, and JPEG are allowed.'}

def test_describe_image_failure():
    image_file = BytesIO(b"mock image data")
    image_file.name = "test.png"
    with patch('ollama.chat', side_effect=Exception("Model failure")):
        response = client.post("/describe-image", files={"file": ("test.png", image_file, "image/png")})
        assert response.status_code == 500
        assert response.json() == {"detail": "Model failure"}

def test_describe_image_real():
    with open("test.png", "rb") as image_file:
        response = client.post(
            "/describe-image",
            files={"file": ("test.png", image_file, "image/png")}
        )
    assert response.status_code == 200
    response_data = response.json()
    assert 'description' in response_data
    assert "screenshot" in response_data["description"]
