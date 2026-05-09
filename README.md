# URL Redirect Test

Simple tool to test Apache mod_rewrite rules by sending real HTTP requests.

## Setup

```bash
pip install -r requirements-dev.txt
```


## Usage

1. Put your test URLs in input/input_urls.tab (one URL per line, tab-separated)
2. Run the script:
   python test_rewrite_results.py
3. Results will be saved in output/checked_urls.tab

## Testing

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov
```

## Files

- test_rewrite_results.py - Main script
- tests/test_rewrite_results.py - Unit tests
- requirements-dev.txt - Development dependencies