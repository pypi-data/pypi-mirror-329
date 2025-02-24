import os
import base64
from openai import OpenAI
from collections.abc import AsyncIterator
from llx.providers.provider import Provider

class OpenAIProvider(Provider):
    def __init__(self, model: str):
        self.model = model
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def invoke(self, prompt: str, attachment: str=None) -> AsyncIterator[str]:
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                ]
            }
        ]
        if attachment:
            with open(attachment, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode("utf-8")

            messages[0]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })

        stream = self.client.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=True
        )    
        for chunk in stream:
            yield chunk.choices[0].delta.content
