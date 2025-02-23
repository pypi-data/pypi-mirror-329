# pastit-cli

A command-line tool for quickly sharing files and text snippets using a Zipline server.

## Features
- Upload files directly from command line
- Upload text from stdin
- Progress bar with upload status
- Configurable file extensions
- Supports custom Zipline servers

## Installation

```bash
pip install pastit-cli
```

## Configuration

Run the setup script to configure your Zipline server URL and authorization token:

```bash
./setup.sh
```

Or manually create a `.env` file with:
```
URL=https://your.server/api/upload
AUTHORIZATION_TOKEN=your_token
DEFAULT_EXTENSION=sh
CONSIDER_FILES_STARTING_WITH_DOT_EXTENSIONLESS=true
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
