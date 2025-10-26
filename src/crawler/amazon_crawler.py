"""Amazon-specific crawler implementation."""

import re
from typing import List, Optional
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from loguru import logger

from src.crawler.base_crawler import BaseCrawler
from src.models.product import Product


class AmazonCrawler(BaseCrawler):
    """Crawler specifically for Amazon.com."""
    
    BASE_URL = "https://www.amazon.com"
    
    def __init__(self):
        """Initialize Amazon crawler."""
        super().__init__()
        logger.info("Amazon crawler initialized")
    
    def search_products(self, keywords: str, pages: int = 1) -> List[Product]:
        """
        Search for products on Amazon.
        
        Args:
            keywords: Search keywords
            pages: Number of pages to crawl
            
        Returns:
            List of Product objects
        """
        all_products = []
        
        for page in range(1, pages + 1):
            logger.info(f"Searching page {page}/{pages} for: {keywords}")
            products = self._search_page(keywords, page)
            
            if not products:
                logger.warning(f"No products found on page {page}")
                break
            
            all_products.extend(products)
            logger.info(f"Found {len(products)} products on page {page}")
        
        logger.info(f"Total products found: {len(all_products)}")
        return all_products
    
    def _search_page(self, keywords: str, page: int) -> List[Product]:
        """
        Search a specific page of results.
        
        Args:
            keywords: Search keywords
            page: Page number (1-indexed)
            
        Returns:
            List of Product objects from the page
        """
        # Build search URL
        url = self._build_search_url(keywords, page)
        
        # Fetch the page
        response = self.fetch(url)
        if not response:
            return []
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Find product containers
        # Amazon uses various data-attribute structures
        products = []
        
        # Try to find product results container
        results = soup.find_all('div', {'data-asin': True, 'data-index': True})
        
        if not results:
            # Alternative selector for Amazon's new layout
            results = soup.find_all('div', class_='s-result-item')
        
        for item in results:
            product = self._parse_product(item)
            if product:
                products.append(product)
        
        return products
    
    def _build_search_url(self, keywords: str, page: int) -> str:
        """
        Build Amazon search URL.
        
        Args:
            keywords: Search keywords
            page: Page number (1-indexed)
            
        Returns:
            Complete search URL
        """
        encoded_keywords = quote_plus(keywords)
        # Amazon uses 'ref=sr_pg_' for pagination
        page_num = page if page == 1 else page
        return f"{self.BASE_URL}/s?k={encoded_keywords}&page={page_num}"
    
    def _parse_product(self, item: BeautifulSoup) -> Optional[Product]:
        """
        Parse a product item from search results.
        
        Args:
            item: BeautifulSoup element containing product data
            
        Returns:
            Product object or None
        """
        try:
            # Extract product name
            title_elem = item.find('h2', class_='a-size-mini') or \
                         item.find('h2', class_='a-size-medium') or \
                         item.find('span', class_='a-size-medium') or \
                         item.find('span', {'data-attribute': True})
            
            if not title_elem:
                # Try alternative selectors
                title_elem = item.find('a', class_='a-link-normal') or \
                           item.find('span', class_='a-text-normal')
            
            product_name = title_elem.get_text(strip=True) if title_elem else "Product name not found"
            
            # Extract brand (often the first word or part of product name)
            brand = None
            # Try to find brand element
            brand_elem = item.find('span', class_='a-color-base') or \
                        item.find('span', class_='a-size-base-plus') or \
                        item.find('span', attrs={'data-component-type': 's-product-spec'})
            
            if brand_elem:
                brand = brand_elem.get_text(strip=True).split()[0] if brand_elem.get_text(strip=True) else None
            
            # If no brand found, try to extract from product name (first word)
            if not brand and product_name and product_name != "Product name not found":
                brand_parts = product_name.split()
                if brand_parts:
                    # Take first 1-2 words as potential brand
                    brand = ' '.join(brand_parts[:2]) if len(brand_parts) > 1 else brand_parts[0]
            
            # Extract price
            price_elem = item.find('span', class_='a-price-whole') or \
                        item.find('span', class_='a-price') or \
                        item.find('span', class_='a-color-price')
            
            price = ""
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                # Clean up price text
                if '$' in price_text:
                    price = price_text.split('$')[-1].strip()
                else:
                    price = price_text
            
            # Extract rating
            rating_elem = item.find('span', class_='a-icon-alt') or \
                         item.find('i', class_='a-icon-star')
            
            rating_text = rating_elem.get_text(strip=True) if rating_elem else ""
            review_score = self._extract_review_score(rating_text)
            
            # Extract number of reviews
            num_reviews_elem = item.find('a', class_='a-link-normal') or \
                             item.find('span', string=re.compile(r'\d+.*rating'))
            
            num_reviews = None
            if num_reviews_elem:
                reviews_text = num_reviews_elem.get_text(strip=True)
                num_reviews = self._extract_num_reviews(reviews_text)
            
            # Extract details/description
            details_elem = item.find('span', class_='a-color-base') or \
                          item.find('div', class_='a-row')
            
            product_details = ""
            if details_elem:
                details_text = details_elem.get_text(strip=True)
                if details_text and len(details_text) > 50:  # Avoid tiny descriptions
                    product_details = details_text[:500]  # Limit length
            
            return Product(
                brand=brand,
                product_name=product_name,
                product_details=product_details,
                review_score=review_score,
                num_reviews=num_reviews,
                price=price,
                rating_text=rating_text
            )
            
        except Exception as e:
            logger.error(f"Error parsing product: {e}")
            return None
    
    def _extract_review_score(self, rating_text: str) -> Optional[float]:
        """
        Extract review score from rating text.
        
        Args:
            rating_text: Rating text (e.g., "4.5 out of 5 stars")
            
        Returns:
            Float score or None
        """
        if not rating_text:
            return None
        
        # Try to extract number from text like "4.5 out of 5 stars"
        match = re.search(r'([\d.]+)', rating_text)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                pass
        
        return None
    
    def _extract_num_reviews(self, reviews_text: str) -> Optional[int]:
        """
        Extract number of reviews from text.
        
        Args:
            reviews_text: Reviews text (e.g., "1,234 ratings")
            
        Returns:
            Integer number of reviews or None
        """
        if not reviews_text:
            return None
        
        # Extract numbers from text like "1,234 ratings" or "1.2K ratings"
        match = re.search(r'([\d,]+)', reviews_text.replace(',', ''))
        if match:
            try:
                return int(match.group(1).replace(',', ''))
            except ValueError:
                pass
        
        # Handle K notation (e.g., 1.2K -> 1200)
        match = re.search(r'([\d.]+)\s*K', reviews_text, re.IGNORECASE)
        if match:
            try:
                value = float(match.group(1))
                return int(value * 1000)
            except ValueError:
                pass
        
        return None

