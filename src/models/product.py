"""Product data models."""

from typing import Optional, List
from pydantic import BaseModel, Field


class Product(BaseModel):
    """Product information model."""
    brand: Optional[str] = Field(default=None, description="Product brand")
    product_name: str = Field(..., description="Product name")
    product_details: Optional[str] = Field(default="", description="Product details/description")
    review_score: Optional[float] = Field(default=None, description="Average review score")
    num_reviews: Optional[int] = Field(default=None, description="Number of reviews")
    price: Optional[str] = Field(default=None, description="Product price")
    rating_text: Optional[str] = Field(default=None, description="Rating text (e.g., '4.5 out of 5 stars')")
    
    def to_csv_row(self) -> List[str]:
        """
        Convert product to CSV row format.
        
        Returns:
            List of strings representing CSV row
        """
        return [
            self.brand or "",
            self.product_name or "",
            self.product_details or "",
            f"{self.review_score:.1f}" if self.review_score else "",
            f"{self.num_reviews}" if self.num_reviews else "",
            self.price or "",
            self.rating_text or ""
        ]

