# py-llama-backend

# Tech choices and reasoning:

This is meant to be an afternoon project, so it's pretty bearbones and the choices prioritize getting something up and running fast and cheap.


## The stack

- Python 3.10
- FastAPI
- Ollama


## Why Python?

For a quick MVP, the simplest languages to get something up and running fast are JS, Python, and Golang. Of those three, Python has the best tooling for interacting with LLMs. All three choices are valid. 

If I really needed performance I'd go with Golang (note, since we chose to run LLMs locally our performance bottleneck is the GPU, not the language. Chosing Golang for perfomance here would be solving imaginary scaling issues)

Javascript if not a bad choice, it's pretty much the only language (Elixir asside) that can do frontend and backend in a sane way. I'd probably go with javascript if this project also required a frontend, just cause it'd be easier to run a single fullstack framework (like nuxt or next)

## Why FastAPI?

It's the quickest way to get a simple and performant API up and running in Python. Django would be a terrible choice for this (too bloated for a one afternoon MVP API with two or three endpoints). Flask would also be ok.


## Why run LLMs locally with Ollama?

The problems we're trying to solve are really simple. We don't need any complicated model, llama3.1 can do text summarization pretty well, and tinyllama text autocomplete. The downside is that our response time will be limited by our GPU. With a very slow GPU, using OpenAI's gpt-3.5-turbo will outperform us, but with a decent GPU, running locally will be faster cause we have one less network roundtrip. Also we don't have to pay for the API. Our only cost is our own server.

If this wasn't an afternoon project, we could consider doing something more cloud-native and using AWS bedrock. 

Setup and Running:
------------------

To get the `py-llama-backend` up and running, follow these steps. This guide assumes you have basic familiarity with Python and command-line operations.

### Prerequisites

1.  **Python 3.10**: Ensure you have Python 3.10 installed on your machine. You can check your Python version by running:
    
    
    `python3 --version`
    
    If Python is not installed, download and install it from [python.org](https://www.python.org/downloads/).
    
2.  **pip**: Make sure `pip` is installed to handle Python packages.
    
3.  **Ollama**: You need to install `Ollama` to run the LLM locally. Visit the [Ollama Download Page](https://ollama.com/download) and follow the instructions to install it on your operating system.
    

### LLM Service Setup

1.  **Install Ollama**: After downloading, follow the installation instructions for your operating system.
    
2.  **Pull the LLM Model**: Use the `ollama` command-line tool to pull the desired LLM model. For this project, we're using `tinyllama`. Run:
    
    
    `ollama pull tinyllama`
    `ollama pull llama3.1`
    `ollama pull stable-code`
    `ollama pull llava:7b`
    
    You can substitute for any model if desired. Just note, the models are pre-saved in `models_config.py`. Make sure to change those to the desired models
    
3.  **Run Ollama Locally**: Start the Ollama service to run the LLM locally.

    
    `ollama serve`
    
    This command will start the Ollama service, making the model available for requests.
    
    *   **Note**: If you encounter an error such as `Error: listen tcp 127.0.0.1:11434: bind: address already in use`, it could be because Ollama is already running. To resolve this:
        
        *   On macOS, check for an Ollama icon in the toolbar and quit the service from there.
        *   Alternatively, use the terminal to find and kill the running process:
            
            
            `pgrep ollama`  # This command finds the process ID for Ollama 
            `kill <process_id>`  # Replace <process_id> with the actual process ID from the above command`
            
        *   Restart the service with `ollama serve`.

### FastAPI Application Setup

1.  **Clone the Repository**: Start by cloning the repository and navigating into the project directory:
    
    
    `git clone https://github.com/yourusername/py-llama-backend.git cd py-llama-backend`
    
2.  **Create a Virtual Environment**: It's good practice to use a virtual environment to manage dependencies. Create and activate a virtual environment with:
    
    
    `` python3 -m venv venv source venv/bin/activate  # On Windows, use `venv\Scripts\activate` ``
    
3.  **Install Dependencies**: Install the required Python packages listed in `requirements.txt`. If `requirements.txt` does not exist, you can create it with `fastapi` and `uvicorn`:
    
    
    `pip install fastapi uvicorn`
    
    Alternatively, install all dependencies in one go:
    

    `pip install -r requirements.txt`
    
4.  **Run the FastAPI Server**: Start the FastAPI server using Uvicorn:
    
    
    `uvicorn main:app --reload`
    
    This command will start the server on `http://127.0.0.1:8000`. The `--reload` flag is useful during development because it automatically reloads the server when you make changes to your code.


## Endpoints

This API exposes endpoints for interacting with the locally hosted LLM models. Below is an explanation of each endpoint, along with example `curl` commands for testing them.

### 1. **Summarize Endpoint**

**URL:** `/summarize`  
**Method:** `POST`  
**Description:** This endpoint receives a long piece of text and returns a summarized version of it. It uses the `llama3.1` model for text summarization.

**Request Body:**

```
{
  "text": "Your long text here."
}
```

Example curl Command:

`curl -X POST "http://127.0.0.1:8000/summarize" -H "Content-Type: application/json" -d '{"text": "Enter your long text here to summarize."}'`


### 2. **Autocomplete Endpoint**

**URL:** `/autocomplete`  
**Method:** `POST`  
**Description:** This endpoint takes a prompt and generates a continuation of the text. It utilizes the `tinyllama` model for text completion.

**Request Body:**
```
{
  "text": "Your initial text here."
}
```

`curl -X POST "http://127.0.0.1:8000/complete" -H "Content-Type: application/json" -d '{"prompt": "Once upon a time in a land far, far away, there was a small village where people lived in harmony. One day, a stranger arrived with a mysterious message. The villagers gathered around to hear what the stranger had to say. The message was..."}'`


### 3. **Generate Code Endpoint**

**URL:** `/generate-code`  
**Method:** `POST`  
**Description:** This endpoint generates code. It can take direct instructions, or incomplete code for the LLM to fill in the gaps

**Request Body:**
```
{
  "text": "Your initial code here."
}
```

`curl -X POST "http://127.0.0.1:8000/generate-code" -H "Content-Type: application/json" -d '{"text": "def print_hello_world():"}`

### 4. **Autocomplete Endpoint**

**URL:** `/describe-image`  
**Method:** `POST`  
**Description:** This endpoint descibres an image. Send and image and get the text description back

```
{
  "image": "Base64 encoded image data here."
}
```

`curl -X POST "http://127.0.0.1:8000/describe-image" -H "Content-Type: multipart/form-data" -F "file=a.png"`


## Testing

To run the tests for the `py-llama-backend` project, you need to have `pytest` installed. If it is not installed, you can add it to your environment with:

`pip install pytest`

To execute the tests, simply run:

`pytest`