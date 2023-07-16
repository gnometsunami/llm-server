import os
from string import Template

import fastapi
import requests
import uvicorn
from pydantic import BaseModel
from requests.exceptions import HTTPError

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
    name=int(os.getenv("PERSONALITY_NAME", "HAL")),
    description="You are a AI assistant that provides factual and helpful answers to a human.",
)


# Show current personality
@api.get("/personality")
async def get_personality():
    return api.personality


# Allow personality to be updated
@api.post("/personality")
async def post_personality(personality: Personality):
    api.personality = personality


# Show current prompt template
@api.get("/template")
async def get_template():
    return api.model_prompt_template


# Allow prompt template to be updated
@api.post("/template")
async def post_template(template: PromptTemplate):
    api.model_prompt_template = Template(template.template)


@api.post("/query")
async def post_prompt(query: Query):
    prompt = api.model_prompt_template.substitute(
        personality=api.personality.description, prompt=query.q
    )
    full_prompt = {"prompt": prompt, "n_predict": 128}

    try:
        response = requests.post(prompt_url, json=full_prompt)
        response.raise_for_status()
        jsonResponse = response.json()
        reply = jsonResponse["content"].lstrip()
        return {"reply": reply}

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")

    except Exception as err:
        print(f"Other error occurred: {err}")


if __name__ == "__main__":
    print("Starting webserver...")
    uvicorn.run(
        api,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 9000)),
        log_level=os.getenv("LOG_LEVEL", "info"),
        proxy_headers=True,
    )
