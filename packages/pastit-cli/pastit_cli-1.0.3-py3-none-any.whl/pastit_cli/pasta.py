import os
import sys
import requests
from dotenv import load_dotenv
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from . import config

console = Console()

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0

class ProgressFileAdapter:
    def __init__(self, filename, task, progress):
        self.filename = filename
        self.task = task
        self.progress = progress
        self._file = open(filename, 'rb')
        self.len = os.path.getsize(filename)
        self._read = 0

    def read(self, size=-1):
        chunk = self._file.read(size)
        self._read += len(chunk)
        self.progress.update(self.task, completed=self._read)
        return chunk

    def close(self):
        self._file.close()

def main():
    # Ensure we have configuration
    config.ensure_config()
    
    # Load environment variables
    load_dotenv()
    
    # Get configuration from environment variables
    url = os.getenv('URL', 'http://localhost:3000/api/upload')
    authorization_token = os.getenv('AUTHORIZATION_TOKEN')
    
    if not authorization_token:
        console.print("[red]Error:[/red] Authorization token not found in .env file")
        sys.exit(1)
    
    if len(sys.argv) != 2:
        console.print("[yellow]Usage:[/yellow] pasta <file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        console.print(f"[red]Error:[/red] File '{file_path}' not found")
        sys.exit(1)

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    
    # Show file info before upload
    info_text = Text()
    info_text.append("File Upload Details\n", style="bold cyan")
    info_text.append(f"Name: ", style="green")
    info_text.append(file_name + "\n")
    info_text.append(f"Size: ", style="green")
    info_text.append(format_size(file_size))
    
    console.print(Panel(info_text, expand=False))
    
    # Prepare headers and files for the request
    headers = {
        'Authorization': authorization_token,
        'Format': 'random',
        'Original-Name': 'true'
    }
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="green", finished_style="green"),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            console=console,
            expand=True
        ) as progress:
            
            task = progress.add_task(f"[cyan]Uploading {file_name}", total=file_size)
            
            # Use our custom adapter to track upload progress
            file_adapter = ProgressFileAdapter(file_path, task, progress)
            
            response = requests.post(
                url,
                headers=headers,
                files={'file': (file_name, file_adapter, 'application/octet-stream')},
                stream=True
            )
            response.raise_for_status()
            
            # Extract file URL from response
            file_url = response.json()['files'][0]
            modified_url = file_url.replace('localhost:3000', 'share.harryeffingpotter.com')
            
            # Show success message with URL
            console.print("\n[green]✓[/green] Upload complete!")
            console.print(Panel(modified_url, title="Share URL", border_style="green"))
            
            # Make sure to close our file adapter
            file_adapter.close()
            
    except requests.exceptions.RequestException as e:
        console.print(f"\n[red]Error:[/red] Upload failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
