# SWECC Email Scraper

A Python CLI tool for analyzing email data in mbox format. This tool helps you extract insights and perform analysis on email archives.

## Features

- Parse mbox format email archives
- Extract email metadata and content
- Perform basic analysis on email data
- Generate reports and statistics

## Installation

```bash
pip install swecc-email-scraper
```

## Usage

```bash
swecc-email-scraper analyze path/to/mailbox.mbox
```

For more detailed usage instructions, run:
```bash
swecc-email-scraper --help
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/swecc-email-scraper.git
cd swecc-email-scraper
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Run linting
ruff check .

# Run type checking
mypy .
```

## License

MIT License - See LICENSE file for details.
