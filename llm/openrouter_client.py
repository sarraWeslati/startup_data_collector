import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def call_llm(prompt, max_tokens=3000):
    """
    Envoie un prompt a OpenRouter et retourne le texte genere.
    """
    response = client.chat.completions.create(
        model="openrouter/owl-alpha",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content
