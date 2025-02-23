import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt
from dotenv import load_dotenv

console = Console()

def format_url(url):
    """Format the URL correctly."""
    # Remove existing /api/upload if it appears
    url = url.strip().rstrip('/')
    url = url.replace('/api/upload', '')
    
    # Add https:// if not present
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
    
    return f"{url}/api/upload"

def ensure_config():
    """Ensure configuration exists, if not, run setup."""
    config_dir = Path.home() / '.config' / 'pastit'
    env_file = config_dir / '.env'
    
    # Try to load existing config
    load_dotenv(env_file)
    if os.getenv('URL') and os.getenv('AUTHORIZATION_TOKEN'):
        return
    
    # No config found, run setup
    console.print("[bold cyan]First-time Pastit Setup[/bold cyan]")
    console.print("This will create a configuration file in your home directory.\n")
    
    # Get user input
    base_url = Prompt.ask("Enter your base share URL (e.g. share.harryeffingpotter.com)")
    url = format_url(base_url)
    
    console.print("\nPlease paste your Zipline authorization token:")
    console.print("Follow along with this 7 second video guide:", 
                 "https://share.harryeffingpotter.com/u/QHqMKf.mp4", style="blue underline")
    authorization_token = Prompt.ask("Authorization token")
    
    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # Create .env file
    with open(env_file, 'w') as f:
        f.write(f"URL={url}\n")
        f.write(f"AUTHORIZATION_TOKEN={authorization_token}\n")
        f.write("DEFAULT_EXTENSION=sh\n")
        f.write("CONSIDER_FILES_STARTING_WITH_DOT_EXTENSIONLESS=true\n")
    
    console.print(f"\n[green]✓[/green] Configuration saved to: {env_file}")
    
    # Load the new config
    load_dotenv(env_file)
