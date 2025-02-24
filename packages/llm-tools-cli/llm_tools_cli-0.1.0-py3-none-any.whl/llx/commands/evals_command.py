import click
from abc import ABC

class EvalsCommand(ABC):
    """Handle evaluation logic"""
    
    def __init__(self, provider: str, model: str):
        self.provider = provider
        self.model = model

    def execute(self, path: str):
        # Implement evals logic here
        click.echo(f"Running evals from {path} with target {self.provider} and model {self.model}")
