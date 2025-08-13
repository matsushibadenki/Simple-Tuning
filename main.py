# main.py
# プロジェクトのメインエントリポイント
import click

@click.group()
def cli():
    """Simple-Tuning: A tool for fine-tuning and serving LLMs."""
    pass

@cli.command()
def train():
    """Run fine-tuning process."""
    from src.simple_tuning.training.trainer import run_training
    run_training()

@cli.command()
def chat_client():
    """Start the chat client."""
    from src.simple_tuning.chat.client import main as client_main
    client_main()

@cli.command()
def start_server():
    """Start the llama.cpp server."""
    from src.simple_tuning.chat.server import start_server as server_main
    server_main()

if __name__ == "__main__":
    cli()