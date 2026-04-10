"""
Price Researcher Module
Researches market prices across platforms
"""

import json
import subprocess
from datetime import datetime


class PriceResearcher:
    """Research prices on eBay, Facebook Marketplace, etc."""
    
    def __init__(self):
        self.platforms = ['ebay', 'facebook', 'mercari', 'offerup']
    
    def research(self, item_data):
        """
        Research market prices for an item
        
        Returns dict with:
        - suggested_price: Recommended price
        - price_range: (min, max) observed prices
        - ebay_sold: Recent eBay sold prices
        - fb_marketplace: Current Facebook listings
        - comp_count: Number of comparables found
        """
        
        title = item_data.get('title', '')
        brand = item_data.get('brand', '')
        category = item_data.get('category', '')
        
        search_query = f"{brand} {title}".strip()
        
        print(f"   Searching: '{search_query}'...")
        
        # Use Hermes web search to find pricing data
        pricing_data = self._search_ebay_sold(search_query)
        
        # Calculate suggested price
        if pricing_data['prices']:
            avg_price = sum(pricing_data['prices']) / len(pricing_data['prices'])
            # Price slightly below average for quick sale
            suggested_price = round(avg_price * 0.85, 2)
        else:
            # Fallback pricing by category
            suggested_price = self._estimate_by_category(category)
        
        return {
            'suggested_price': suggested_price,
            'price_range': (min(pricing_data['prices']) if pricing_data['prices'] else 0,
                          max(pricing_data['prices']) if pricing_data['prices'] else 0),
            'comp_count': len(pricing_data['prices']),
            'ebay_sold_prices': pricing_data['prices'][:5],  # Top 5
            'research_date': datetime.now().isoformat(),
            'search_query': search_query
        }
    
    def _search_ebay_sold(self, query):
        """Search eBay sold listings for comparable prices"""
        
        # Simulate eBay search (in production, use eBay API or web scraping)
        # For MVP, we'll use Hermes web_search tool
        
        try:
            # Use Hermes to search
            result = subprocess.run(
                ['hermes', 'chat', '-q', 
                 f'Search eBay sold listings for "{query}" and extract the last 5 sold prices'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse prices from response (simplified for MVP)
            # In production, parse actual pricing data
            prices = [29.99, 34.99, 27.50, 32.00, 30.00]  # Mock data
            
        except Exception as e:
            print(f"   Warning: eBay search failed ({e}), using estimates")
            prices = []
        
        return {'prices': prices}
    
    def _estimate_by_category(self, category):
        """Fallback pricing estimates by category"""
        estimates = {
            'Electronics': 45.00,
            'Furniture': 75.00,
            'Tools': 30.00,
            'Collectibles': 25.00,
            'Clothing': 15.00,
            'Household': 12.00,
            'Toys': 10.00,
            'Books': 8.00,
            'Appliances': 50.00,
            'Sporting Goods': 35.00,
            'Jewelry': 40.00,
            'Art': 60.00,
            'Musical Instruments': 100.00,
            'General': 20.00
        }
        return estimates.get(category, 20.00)
