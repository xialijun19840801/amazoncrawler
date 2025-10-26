# Quick Start Guide

## Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the crawler:**
```bash
python main.py
```

## Usage Example

```bash
$ python main.py

=== Amazon Product Crawler ===

Enter search keywords: laptop
Enter number of pages to crawl (1-10): 2

[INFO] Starting crawl for: laptop
[INFO] Pages to crawl: 2
[INFO] Searching page 1/2 for: laptop
[INFO] Found 24 products on page 1
[INFO] Searching page 2/2 for: laptop
[INFO] Found 24 products on page 2
[INFO] Total products found: 48
[INFO] Successfully exported 48 products to output/amazon_products_laptop_20240101_120000.csv
[INFO] ✓ Crawl completed successfully!
[INFO] ✓ Found 48 products
[INFO] ✓ Exported to: output/amazon_products_laptop_20240101_120000.csv
```

## CSV Output

The crawler creates a CSV file in the `output/` directory with the following columns:
- **Brand:** Product brand/manufacturer
- **Product Name:** The product name
- **Product Details:** Product description/details
- **Review Score:** Average rating (e.g., 4.5)
- **Number of Reviews:** Total number of reviews

Example output file: `amazon_products_laptop_20240101_120000.csv`

## Configuration

Optionally create a `.env` file for custom settings:

```env
REQUEST_DELAY=2.0
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

## Features

✅ Respects rate limits (2 second delay between requests)  
✅ Automatic retry on failures  
✅ Comprehensive logging  
✅ Clean CSV export with brand information  
✅ Multiple pages support  
✅ Error handling

## Tips

- Keep page count reasonable (1-5 pages works best)
- The crawler includes a 2-second delay to be respectful
- Check the logs/ directory for detailed logs
- Output files include timestamps in the filename
