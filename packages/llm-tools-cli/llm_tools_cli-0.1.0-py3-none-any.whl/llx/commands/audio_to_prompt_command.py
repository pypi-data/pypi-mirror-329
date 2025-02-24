from typing import Optional
import click
from abc import ABC

class AudioToPromptCommand(ABC):
    """Handle audio processing and prompt generation"""
    
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model

    def execute(self, path: str, prompt: Optional[str]):
        # Implement speech-to-text logic here
        click.echo(f"Processing audio from {path} with prompt {prompt}")
