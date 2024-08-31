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
    
    You can substitute `tinyllama` and `llama3.1` with another model if desired.
    
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


`curl -X POST "http://127.0.0.1:8000/summarize" -H "Content-Type: application/json" -d '{"text": "Enter your long text here to summarize."}'`



```
curl -X POST "http://127.0.0.1:8000/summarize" -H "Content-Type: application/json" -d '{"text": "Software engineers are not (and should not be) technicians. I don’t actually think predictability is a good thing in software engineering. This will probably come as a surprise to some people (especially managers), but I’ll explain what I mean. In my view, a great software engineer is one who automates repetitive/manual labor. You would think that this is a pretty low bar to clear, right? Isn’t automation of repetitive tasks … like … programming 101? Wouldn’t most software engineers be great engineers according to my criterion? No. I would argue that most large software engineering organizations incentivize anti-automation and it’s primarily because of their penchant for predictability, especially predictable estimates and predictable work. The reason this happens is that predictable work is work that could have been automated but was not automated. Example: I’ll give a concrete example of predictable work from my last job. Early on we had a dedicated developer for maintaining our web API. Every time some other team added a new gRPC API endpoint to an internal service this developer was tasked with exposing that same information via an HTTP API. This was a fairly routine job but it still required time and thought on their part. Initially managers liked the fact that this developer could estimate reliably (because the work was well-understood) and this developer liked the fact that they didn’t have to leave their comfort zone. But it wasn’t great for the business! This person frequently became a bottleneck for releasing new features because they had inserted their own manual labor as a necessary step in the development pipeline. They made the case that management should hire more such developers like themselves to handle increased demand for their work. Our team pushed back on this because we recognized that this developer’s work was so predictable that it could be completely automated. We made the case to management that rather than hiring another person to do the same work we should be automating more and it’s a good thing we did; that developer soon left the company and instead of hiring to replace them we automated away their job instead. We wrote some code to automatically generate an HTTP API from the corresponding gRPC API and that generated much more value for the business than hiring a new developer. Technicians vs Engineers: I like to use the term “technician” to describe a developer who (A) does work that is well-understood and (B) doesn’t need to leave their comfort zone very often. Obviously there is not a bright line dividing engineers from technicians, but generally speaking the more predictable and routine a developer’s job the more they tend to slide into becoming a technician. In the above example, I viewed the developer maintaining the web API as more of a technician than an engineer. In contrast, the more someone leans into being an engineer the more unpredictable their work gets (along with their estimates). If you’re consistently automating things then all of the predictable work slowly dries up and all that’s left is unpredictable work. The nature of a software engineer’s job is that they are tackling increasingly challenging and ambitious tasks as they progressively automate more. I believe that most tech companies should not bias towards predictability and should avoid hiring/cultivating technicians. The reason that tech companies command outsized valuations is because of automation. Leaning into predictability and well-understood work inadvertently incentivizes manual labor instead of automation. This isn’t obvious to a lot of tech companies because they assume any work involving code is necessarily automation but that’s not always the case. Tech companies that fail to recognize this end up over-hiring and wondering why less work is getting done with more people. Or to put it another way: I actually view it as a red flag if an engineer or team gets into a predictable “flow” because it means that there is a promising opportunity for automation they’re ignoring."}'
```

