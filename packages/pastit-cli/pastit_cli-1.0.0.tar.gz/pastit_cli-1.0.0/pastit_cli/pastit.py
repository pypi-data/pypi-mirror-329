import os
import sys
import tempfile
import requests
from dotenv import load_dotenv
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TransferSpeedColumn
from rich import print as rprint

console = Console()

def get_input():
    """Get input from either file argument or stdin"""
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], 'r') as f:
                return f.read(), Path(sys.argv[1]).name
        except Exception as e:
            console.print(f"[red]Error:[/red] Could not read file: {str(e)}")
            sys.exit(1)
    elif not sys.stdin.isatty():
        return sys.stdin.read(), "input.txt"
    else:
        console.print("[yellow]Usage:[/yellow] pastit <file> or echo 'text' | pastit")
        sys.exit(1)

def get_filename_with_extension(filename):
    """Add default extension to files without extension or dot files if configured"""
    load_dotenv()
    default_extension = os.getenv('DEFAULT_EXTENSION', 'sh')
    consider_dot_files = os.getenv('CONSIDER_FILES_STARTING_WITH_DOT_EXTENSIONLESS', 'true').lower() == 'true'
    
    if '.' not in filename or (consider_dot_files and filename.startswith('.')):
        return f"{filename}.{default_extension}"
    return filename

def get_syntax_theme():
    """Get syntax highlighting theme based on terminal background"""
    if console.color_system is None:
        return "default"
    return "monokai"

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0

def main():
    # Load environment variables
    load_dotenv()
    
    # Get configuration
    url = os.getenv('URL', 'http://localhost:3000/api/upload')
    authorization_token = os.getenv('AUTHORIZATION_TOKEN')
    
    if not authorization_token:
        console.print("[red]Error:[/red] Authorization token not found in .env file")
        sys.exit(1)
    
    # Get input content and filename
    content, original_filename = get_input()
    filename = get_filename_with_extension(original_filename)
    
    # Show preview of content
    preview_text = Text()
    preview_text.append("Content Preview\n", style="bold cyan")
    
    # Truncate content for preview if it's too long
    preview_content = content[:500] + "..." if len(content) > 500 else content
    syntax = Syntax(preview_content, "python", theme=get_syntax_theme(), line_numbers=True)
    
    console.print(Panel(syntax, title=f"[green]{filename}[/green]", expand=False))
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix=f'_{filename}', delete=False) as temp_file:
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # Prepare headers and files for the request
        headers = {
            'Authorization': authorization_token,
            'Format': 'random',
            'Original-Name': 'true'
        }
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(complete_style="green", finished_style="green"),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TransferSpeedColumn(),
            console=console,
            expand=True
        ) as progress:
            
            upload_task = progress.add_task("[cyan]Uploading content", total=1)
            
            with open(temp_path, 'rb') as file:
                progress.update(upload_task, advance=0.2)
                
                response = requests.post(
                    url,
                    headers=headers,
                    files={'file': (filename, file, 'application/octet-stream')}
                )
                response.raise_for_status()
                
                progress.update(upload_task, advance=0.8)
                
                # Extract and modify file URL from response
                file_url = response.json()['files'][0]
                modified_url = file_url.replace('/u/', '/code/')
                
                # Show success message with URL
                console.print("\n[green]✓[/green] Upload complete!")
                console.print(Panel(
                    Text(modified_url, style="blue underline"),
                    title="[green]Share URL[/green]",
                    border_style="green"
                ))
            
    except requests.exceptions.RequestException as e:
        console.print(f"\n[red]Error:[/red] Upload failed: {str(e)}")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except:
            pass

if __name__ == "__main__":
    main()
