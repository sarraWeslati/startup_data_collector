import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY introuvable. "
        "Cree un fichier .env avec OPENROUTER_API_KEY=ta_cle_openrouter"
    )

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def call_llm(prompt, max_tokens=3000):
    response = client.chat.completions.create(
        model="mistralai/mistral-small-3.2-24b-instruct",
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