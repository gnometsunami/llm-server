import os

import fastapi
import uvicorn
import requests
from requests.exceptions import HTTPError
from pydantic import BaseModel
from string import Template

prompt_url = os.environ.get("PROMPT_URL", "http://llm:8080/completion")

class Personality(BaseModel):
    name: str
    description: str

class Query(BaseModel):
    q: str

class PromptTemplate(BaseModel):
    template: str

api = fastapi.FastAPI()

api.model_prompt_template = Template("$personality\n\nUSER: $prompt \nASSISTANT:")

api.personality = Personality(
    name="Alucard",
    description="Your name is Adrian Fahrenheit Ţepeş, a half-vampire, better known as Alucard. Your father was Dracula and your mother was Lisa Fahrenheit. You are highly intelligent, cunning, brooding, and stoic. You will answer the questions of a human visiting your castle. Write one sentence answers."
)

# Show current personality
@api.get("/personality")
async def personality():
    return api.personality

# Allow personality to be updated
@api.post("/personality")
async def personality(personality: Personality):
    api.personality = personality

# Show current prompt template
@api.get("/template")
async def template():
    return api.model_prompt_template

# Allow prompt template to be updated
@api.post("/template")
async def template(template: PromptTemplate):
    api.model_prompt_template = Template(template.template)

@api.post("/query")
async def prompt(query: Query):

    prompt = api.model_prompt_template.substitute(personality=api.personality.description, prompt=query.q)
    full_prompt = { "prompt": prompt, "n_predict": 128 }

    try:
        response = requests.post(prompt_url, json=full_prompt)
        response.raise_for_status()
        jsonResponse = response.json()
        reply = jsonResponse["content"].lstrip()
        return { "reply": reply }
    
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')

    except Exception as err:
        print(f'Other error occurred: {err}')

if __name__ == "__main__":
    print("Starting webserver...")
    uvicorn.run(
        api,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 9000)),
        log_level=os.getenv("LOG_LEVEL", "info"),
        proxy_headers=True,
    )