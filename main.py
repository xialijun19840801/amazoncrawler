"""Main entry point for Amazon crawler."""

import sys
import csv
from pathlib import Path
from datetime import datetime
from loguru import logger

from src.utils.logger import setup_logger
from src.crawler.amazon_crawler import AmazonCrawler
from src.models.product import Product


def export_to_csv(products: list[Product], filename: str) -> None:
    """
    Export products to CSV file.
    
    Args:
        products: List of Product objects
        filename: Output filename
    """
    if not products:
        logger.warning("No products to export")
        return
    
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    filepath = output_dir / filename
    
    # Define CSV headers based on the updated CSV format
    headers = ["Brand", "Product Name", "Product Details", "Review Score", "Number of Reviews"]
    
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for product in products:
                # Map product fields to CSV columns
                row = [
                    product.brand or "",
                    product.product_name or "",
                    product.product_details or "",
                    f"{product.review_score:.1f}" if product.review_score else "",
                    f"{product.num_reviews}" if product.num_reviews else ""
                ]
                writer.writerow(row)
        
        logger.info(f"Successfully exported {len(products)} products to {filepath}")
        
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")
        raise


def main():
    """Main function to run the Amazon crawler."""
    setup_logger()
    
    try:
        # Get user input
        logger.info("=== Amazon Product Crawler ===")
        keywords = input("\nEnter search keywords: ").strip()
        
        if not keywords:
            logger.error("Keywords cannot be empty")
            sys.exit(1)
        
        while True:
            try:
                pages_str = input("Enter number of pages to crawl (1-10): ").strip()
                pages = int(pages_str)
                if 1 <= pages <= 10:
                    break
                else:
                    logger.warning("Please enter a number between 1 and 10")
            except ValueError:
                logger.warning("Please enter a valid number")
        
        # Initialize crawler
        crawler = AmazonCrawler()
        
        try:
            # Search products
            logger.info(f"Starting crawl for: {keywords}")
            logger.info(f"Pages to crawl: {pages}")
            
            products = crawler.search_products(keywords, pages)
            
            if not products:
                logger.warning("No products found. Please check your search terms.")
                sys.exit(1)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            sanitized_keywords = keywords.replace(" ", "_").replace("/", "_")[:50]
            filename = f"amazon_products_{sanitized_keywords}_{timestamp}.csv"
            
            # Export to CSV
            export_to_csv(products, filename)
            
            logger.info(f"\n✓ Crawl completed successfully!")
            logger.info(f"✓ Found {len(products)} products")
            logger.info(f"✓ Exported to: output/{filename}")
            
        finally:
            # Close crawler session
            crawler.close()
    
    except KeyboardInterrupt:
        logger.warning("\nCrawl interrupted by user")
        sys.exit(1)
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
