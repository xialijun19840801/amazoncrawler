# Amazon Product Crawler

A lightweight, ethical web crawler for scraping Amazon product information. This crawler respects rate limits and follows best practices for web scraping.

## Features

- 🔍 Search Amazon products by keywords
- 📄 Crawl multiple pages of results
- 📊 Export data to CSV format with brand information
- 🛡️ Built-in rate limiting (2 seconds between requests)
- 📝 Comprehensive logging
- 🔄 Automatic retry on failures
- ✅ Proper error handling

## CSV Output Format

The crawler exports data in the following CSV format:

| Column | Description |
|--------|-------------|
| Brand | Product brand/manufacturer |
| Product Name | The product name/title |
| Product Details | Product description/details |
| Review Score | Average rating (e.g., 4.5) |
| Number of Reviews | Total number of reviews |

## Installation

1. Clone this repository or navigate to the project directory:
```bash
cd "amazon crawler"
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the crawler with:
```bash
python main.py
```

The program will prompt you for:
1. **Search keywords**: What products to search for (e.g., "laptop", "wireless headphones")
2. **Number of pages**: How many pages to crawl (1-10)

### Example

```bash
$ python main.py

=== Amazon Product Crawler ===

Enter search keywords: wireless headphones
Enter number of pages to crawl (1-10): 3

[INFO] Starting crawl for: wireless headphones
[INFO] Pages to crawl: 3
[INFO] Searching page 1/3 for: wireless headphones
[INFO] Found 24 products on page 1
[INFO] Searching page 2/3 for: wireless headphones
[INFO] Found 24 products on page 2
...
[INFO] ✓ Crawl completed successfully!
[INFO] ✓ Found 72 products
[INFO] ✓ Exported to: output/amazon_products_wireless_headphones_20240101_120000.csv
```

Output files are saved in the `output/` directory with a timestamp.

## Configuration

Create a `.env` file in the project root to customize settings (optional):

```env
# Delay between requests (seconds)
REQUEST_DELAY=2.0

# Request timeout (seconds)
REQUEST_TIMEOUT=30

# Maximum retry attempts
MAX_RETRIES=3

# Output directory
OUTPUT_DIR=output
```

## Project Structure

```
amazon crawler/
├── src/
│   ├── crawler/
│   │   ├── __init__.py
│   │   ├── base_crawler.py      # Base crawler with HTTP session
│   │   └── amazon_crawler.py   # Amazon-specific crawling logic
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py           # Product data models
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py            # Logging configuration
│   │   └── rate_limiter.py     # Rate limiting utility
│   └── config/
│       ├── __init__.py
│       └── settings.py          # Application settings
├── tests/                        # Unit tests
├── output/                       # Generated CSV files
├── logs/                         # Application logs
├── main.py                       # Main entry point
├── requirements.txt              # Python dependencies
├── .cursorrules                  # Cursor IDE rules
├── .env.example                  # Example environment variables
└── README.md                     # This file
```

## Legal & Ethical Guidelines

⚠️ **Important**: This crawler is designed for educational and research purposes only.

- Always respects Amazon's robots.txt and rate limits
- Implements proper delays between requests (minimum 2 seconds)
- Uses User-Agent headers that identify the crawler
- Never overloads Amazon's servers
- Complies with Amazon's Terms of Service

**Please note**: Web scraping may violate website Terms of Service. Use at your own risk and ensure compliance with applicable laws and website policies. For production use, consider using Amazon's official APIs.

## Troubleshooting

### No products found
- Verify your search keywords are correct
- Amazon may have changed their HTML structure
- Try different keywords or fewer pages

### Connection errors
- Check your internet connection
- Amazon may be temporarily blocking requests
- Wait a few minutes and try again

### Rate limiting
- The crawler already implements a 2-second delay
- If you're still being blocked, increase the delay in settings.py
- Consider using fewer pages per crawl

## Dependencies

- **requests**: HTTP library for making requests
- **beautifulsoup4**: HTML parsing
- **lxml**: Fast XML/HTML parser
- **pydantic**: Data validation
- **python-dotenv**: Environment variables
- **loguru**: Enhanced logging

## Development

To contribute or modify the crawler:

1. Make changes to the source code in `src/`
2. Test your changes
3. Run linters and formatters:
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## License

This project is for educational purposes only.

## Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for ensuring they comply with Amazon's Terms of Service and applicable laws when using this software.
