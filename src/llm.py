import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Get the GitHub token from environment variables
# Note: While the variable is GITHUB_TOKEN, it's used as the API key for the specified endpoint.
api_key = os.getenv("GITHUB_TOKEN")

# Configure the OpenAI client
client = openai.OpenAI(
    api_key=api_key,
    base_url="https://models.inference.ai.azure.com",
)

def call_llm_model(model, messages, temperature=1.0, top_p=1.0):
    """
    Calls the specified language model with the given parameters.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def translate_note(note, target_lang):
    """
    Translates a given note to the target language. target_lang should be 'en' or 'zh'.
    """
    lang_map = {"en": "English", "zh": "Chinese"}
    target = lang_map.get(target_lang, target_lang)
    messages = [
        {"role": "system", "content": "You are a precise translation assistant. Return only the translated text without explanations."},
        {"role": "user", "content": f"Translate the following text to {target}: \n\n{note}"}
    ]
    return call_llm_model("gpt-4.1-mini", messages)

if __name__ == "__main__":
    note_to_translate = "Hello"
    target_language = "zh"
    print(f"Translating '{note_to_translate}' to {target_language}...")
    translated_text = translate_note(note_to_translate, target_language)
    if translated_text:
        print(f"Translation: {translated_text}")
    else:
        print("Translation failed.")