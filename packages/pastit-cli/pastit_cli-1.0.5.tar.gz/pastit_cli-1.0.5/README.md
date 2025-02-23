# pastit-cli

A command-line tool for quickly sharing files and text snippets using a Zipline server.

## Features
- Upload files directly from command line
- Upload text from stdin
- Progress bar with upload status
- Configurable file extensions
- Supports custom Zipline servers
- Automatic first-time setup

## Installation

```bash
pip install pastit-cli
```

## Usage

Upload a file:
```bash
pasta filename.txt
```

Upload from stdin:
```bash
echo "Hello World" | pastit
```

Or pipe any command output:
```bash
ls -la | pastit
```

On first run, you'll be prompted to enter your:
- Zipline server URL
- Authorization token

Your configuration will be saved in `~/.config/pastit/.env` and will be used for future uploads.

## Manual Configuration

If you need to change your configuration, you can either:

1. Edit `~/.config/pastit/.env` directly:
```ini
URL=https://your.server/api/upload
AUTHORIZATION_TOKEN=your_token
DEFAULT_EXTENSION=sh
CONSIDER_FILES_STARTING_WITH_DOT_EXTENSIONLESS=true
```

2. Or run the setup command:
```bash
pastit-setup
```
