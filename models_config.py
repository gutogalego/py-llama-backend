# models_config.py

# Model names for different tasks
LLM_SUMMARIZATION_MODEL = 'llama3.1'
LLM_AUTOCOMPLETE_MODEL = 'tinyllama'
LLM_CODE_GENERATION_MODEL = 'stable-code'
LLM_IMAGE_DESCRIPTION_MODEL = 'llava:7b'

# Pre-prompts for different tasks
PROMPT_SUMMARIZE_TEXT = "Summarize the following text: "
PROMPT_AUTOCOMPLETE_TEXT = "Autocomplete the following sentence. Just the sentence, nothing more: "
PROMPT_DESCRIBE_IMAGE = "Describe this image:"
