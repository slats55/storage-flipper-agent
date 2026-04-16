"""
Listing Generator Module
Creates optimized listings for multiple platforms
"""

import logging
from datetime import datetime

logger = logging.getLogger("flipper.listing_generator")


class ListingGenerator:
    """Generate platform-specific listings"""
    
    def __init__(self):
        self.platforms = {
            'ebay': self._generate_ebay_listing,
            'facebook': self._generate_facebook_listing,
            'mercari': self._generate_mercari_listing,
            'offerup': self._generate_offerup_listing
        }
    
    def generate(self, item_data):
        """
        Generate listings for all platforms
        
        Returns dict of platform: listing_data
        """
        listings = {}
        
        for platform, generator_func in self.platforms.items():
            try:
                listing = generator_func(item_data)
                listings[platform] = listing
                print(f"      ✓ {platform}")
            except Exception as e:
                logger.warning("Listing failed for platform=%s: %s", platform, e, exc_info=True)
                print(f"      ✗ {platform}: {e}")
        
        return listings
    
    def _generate_ebay_listing(self, item_data):
        """Generate eBay-optimized listing"""
        title = self._create_title(item_data, max_chars=80)
        description = self._create_description(item_data, platform='ebay')
        
        return {
            'platform': 'ebay',
            'title': title,
            'description': description,
            'price': item_data.get('suggested_price', 0),
            'condition': self._map_condition_ebay(item_data.get('condition', 'Good')),
            'category': item_data.get('category', 'Other'),
            'shipping': self._suggest_shipping(item_data),
            'photos': [item_data.get('photo_path', '')],
            'listing_type': 'fixed_price',  # or 'auction'
            'duration': '7_days'
        }
    
    def _generate_facebook_listing(self, item_data):
        """Generate Facebook Marketplace listing"""
        title = self._create_title(item_data, max_chars=100)
        description = self._create_description(item_data, platform='facebook')
        
        return {
            'platform': 'facebook',
            'title': title,
            'description': description,
            'price': item_data.get('suggested_price', 0),
            'condition': self._map_condition_facebook(item_data.get('condition', 'Good')),
            'category': item_data.get('category', 'Other'),
            'photos': [item_data.get('photo_path', '')],
            'pickup_only': self._suggest_pickup_only(item_data)
        }
    
    def _generate_mercari_listing(self, item_data):
        """Generate Mercari listing"""
        title = self._create_title(item_data, max_chars=80)
        description = self._create_description(item_data, platform='mercari')
        
        return {
            'platform': 'mercari',
            'title': title,
            'description': description,
            'price': item_data.get('suggested_price', 0),
            'condition': self._map_condition_mercari(item_data.get('condition', 'Good')),
            'category': item_data.get('category', 'Other'),
            'photos': [item_data.get('photo_path', '')],
            'shipping_paid_by': 'buyer'
        }
    
    def _generate_offerup_listing(self, item_data):
        """Generate OfferUp listing"""
        title = self._create_title(item_data, max_chars=80)
        description = self._create_description(item_data, platform='offerup')
        
        return {
            'platform': 'offerup',
            'title': title,
            'description': description,
            'price': item_data.get('suggested_price', 0),
            'condition': item_data.get('condition', 'Good'),
            'category': item_data.get('category', 'Other'),
            'photos': [item_data.get('photo_path', '')],
            'shipping_available': False  # Local pickup default
        }
    
    def _create_title(self, item_data, max_chars=80):
        """Create SEO-optimized title"""
        parts = []
        
        # Brand first (if available)
        brand = item_data.get('brand', '')
        if brand and brand != 'Unknown':
            parts.append(brand)
        
        # Item title
        title = item_data.get('title', 'Item')
        parts.append(title)
        
        # Model number (if available)
        model = item_data.get('model', '')
        if model:
            parts.append(model)
        
        # Condition
        condition = item_data.get('condition', '')
        if condition:
            parts.append(f"- {condition}")
        
        # Join and truncate
        full_title = ' '.join(parts)
        if len(full_title) > max_chars:
            full_title = full_title[:max_chars-3] + '...'
        
        return full_title
    
    def _create_description(self, item_data, platform='ebay'):
        """Create compelling description"""
        lines = []
        
        # Opening
        title = item_data.get('title', 'Item')
        lines.append(f"📦 {title} for Sale!\n")
        
        # Condition
        condition = item_data.get('condition', 'Good')
        lines.append(f"Condition: {condition}")
        
        # Features
        features = item_data.get('features', [])
        if features:
            lines.append("\nFeatures:")
            for feature in features:
                lines.append(f"• {feature}")
        
        # Brand/Model
        brand = item_data.get('brand', '')
        model = item_data.get('model', '')
        if brand and brand != 'Unknown':
            lines.append(f"\nBrand: {brand}")
        if model:
            lines.append(f"Model: {model}")
        
        # Call to action
        if platform == 'facebook':
            lines.append("\n💬 Message me with any questions!")
            lines.append("🚗 Local pickup available")
        elif platform == 'ebay':
            lines.append("\n📮 Fast shipping!")
            lines.append("✅ Check out my other listings")
        
        lines.append("\n⭐ From a smoke-free storage unit")
        
        return '\n'.join(lines)
    
    def _map_condition_ebay(self, condition):
        """Map to eBay condition values"""
        mapping = {
            'New': 'New',
            'Like New': 'Like New',
            'Good': 'Good',
            'Fair': 'Acceptable',
            'Poor': 'For parts or not working'
        }
        return mapping.get(condition, 'Used')
    
    def _map_condition_facebook(self, condition):
        """Map to Facebook condition values"""
        mapping = {
            'New': 'new',
            'Like New': 'like_new',
            'Good': 'good',
            'Fair': 'fair',
            'Poor': 'poor'
        }
        return mapping.get(condition, 'good')
    
    def _map_condition_mercari(self, condition):
        """Map to Mercari condition values"""
        mapping = {
            'New': 'new',
            'Like New': 'like_new',
            'Good': 'good',
            'Fair': 'fair',
            'Poor': 'poor'
        }
        return mapping.get(condition, 'good')
    
    def _suggest_shipping(self, item_data):
        """Suggest shipping method based on item"""
        category = item_data.get('category', '')
        
        if category in ['Furniture', 'Appliances']:
            return 'local_pickup'
        else:
            return 'calculated'
    
    def _suggest_pickup_only(self, item_data):
        """Determine if item should be pickup only"""
        category = item_data.get('category', '')
        return category in ['Furniture', 'Appliances', 'Large Items']
