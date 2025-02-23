import os
import sys
import requests
from dotenv import load_dotenv
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from . import config

# New helper function for custom multipart/form-data streaming
def multipart_stream(file_path, file_name, progress, task, boundary, chunk_size=8192):
    CRLF = '\r\n'
    header = (f'--{boundary}{CRLF}'
              f'Content-Disposition: form-data; name="file"; filename="{file_name}"{CRLF}'
              f'Content-Type: application/octet-stream{CRLF}{CRLF}').encode('utf-8')
    footer = (f'{CRLF}--{boundary}--{CRLF}').encode('utf-8')
    # Compute total length and update progress task
    total_length = len(header) + os.path.getsize(file_path) + len(footer)
    progress.update(task, total=total_length)
    yield header
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            progress.update(task, advance=len(chunk), refresh=True)
            yield chunk
    yield footer

console = Console()

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0

def main():
    # Ensure configuration exists
    config.ensure_config()
    
    # Load environment variables
    load_dotenv()
    
    # Retrieve settings from environment variables
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
    
    # Display file information before upload
    info_text = Text()
    info_text.append("File Upload Details\n", style="bold cyan")
    info_text.append("Name: ", style="green")
    info_text.append(file_name + "\n")
    info_text.append("Size: ", style="green")
    info_text.append(format_size(file_size))
    console.print(Panel(info_text, expand=False))
    
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
            expand=True,
            refresh_per_second=10
        ) as progress:
            task = progress.add_task(f"[cyan]Uploading {file_name}", total=0)
            
            # Set up custom multipart/form-data stream
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            headers['Content-Type'] = f'multipart/form-data; boundary={boundary}'
            header_bytes = (f'--{boundary}\r\n'
                            f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
                            f'Content-Type: application/octet-stream\r\n\r\n').encode('utf-8')
            footer_bytes = (f'\r\n--{boundary}--\r\n').encode('utf-8')
            content_length = len(header_bytes) + os.path.getsize(file_path) + len(footer_bytes)
            headers['Content-Length'] = str(content_length)
            
            # Use the custom multipart stream generator
            stream = multipart_stream(file_path, file_name, progress, task, boundary)
            
            response = requests.post(
                url,
                headers=headers,
                data=stream,
                stream=True
            )
            response.raise_for_status()
            
            # Extract file URL from the response and modify if needed
            file_url = response.json()['files'][0]
            modified_url = file_url.replace('localhost:3000', 'share.harryeffingpotter.com')
            
            console.print("\n[green]✓[/green] Upload complete!")
            console.print(Panel(modified_url, title="Share URL", border_style="green"))
    except requests.exceptions.RequestException as e:
        console.print(f"\n[red]Error:[/red] Upload failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] An unexpected error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()