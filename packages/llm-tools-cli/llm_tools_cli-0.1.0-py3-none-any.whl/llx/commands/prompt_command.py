from abc import ABC
import asyncio
import click
import sys
from typing import Optional
from llx.utils import get_provider

class PromptCommand(ABC):
    """Handle the prompt command logic"""
    
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model
        self.client = get_provider(provider, model)

    async def _print_stream(self, stream):
        async for chunk in stream:
            click.echo(chunk, nl=False)

    def _validate_prompt(self, prompt: Optional[str]) -> str:
        if not prompt:
            if not sys.stdin.isatty():
                prompt = sys.stdin.read().strip()
            
        if not prompt:
            raise click.UsageError("Prompt is required either as an argument or via stdin.")
        return prompt

    def _validate_attachment(self, attachment: Optional[str]):
        if attachment and not attachment.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            raise click.FileError("Attachment must be an image file.")

    def execute(self, prompt: Optional[str], attachment: Optional[str]):
        prompt = self._validate_prompt(prompt)
        self._validate_attachment(attachment)
        asyncio.run(self._print_stream(self.client.invoke(prompt, attachment)))
