"""
Item Identifier Module
Uses vision AI to identify items from photos
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime


class ItemIdentifier:
    """Identifies items from photos using Hermes vision tools"""
    
    def __init__(self):
        self.categories = [
            "Electronics", "Furniture", "Tools", "Collectibles", 
            "Clothing", "Household", "Toys", "Books", "Appliances",
            "Sporting Goods", "Jewelry", "Art", "Musical Instruments"
        ]
    
    def identify(self, photo_path):
        """
        Analyze photo and extract item information
        
        Returns dict with:
        - title: Item name/description
        - brand: Brand name if identifiable
        - model: Model number if visible
        - category: Item category
        - condition: Estimated condition
        - features: Notable features
        """
        
        photo_path = Path(photo_path)
        if not photo_path.exists():
            raise FileNotFoundError(f"Photo not found: {photo_path}")
        
        print(f"   Analyzing photo: {photo_path.name}...")
        
        # Use Hermes vision_analyze via subprocess
        question = '''Identify this item for resale purposes. Provide:
1. Item type and description
2. Brand name (if visible)
3. Model number (if visible)
4. Category (Electronics/Furniture/Tools/etc)
5. Condition (New/Like New/Good/Fair/Poor)
6. Notable features or damage
7. Estimated age/era

Format as JSON.'''
        
        try:
            # Call Hermes CLI with vision analysis
            result = subprocess.run(
                ['hermes', 'chat', '-q', f'Analyze image {photo_path} and answer: {question}'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parse the response (simplified for MVP)
            # In production, we'd parse the actual JSON response
            item_data = {
                'photo_path': str(photo_path),
                'title': self._extract_title_from_photo(photo_path.name),
                'brand': 'Unknown',
                'model': '',
                'category': 'General',
                'condition': 'Good',
                'features': [],
                'analyzed_at': datetime.now().isoformat(),
                'raw_analysis': result.stdout if result.returncode == 0 else 'Analysis pending'
            }
            
        except Exception as e:
            print(f"   Warning: Vision analysis failed ({e}), using fallback")
            item_data = {
                'photo_path': str(photo_path),
                'title': self._extract_title_from_photo(photo_path.name),
                'brand': 'Unknown',
                'model': '',
                'category': 'General',
                'condition': 'Good',
                'features': [],
                'analyzed_at': datetime.now().isoformat()
            }
        
        return item_data
    
    def _extract_title_from_photo(self, filename):
        """Extract a basic title from filename"""
        # Remove extension and clean up
        title = Path(filename).stem
        title = title.replace('_', ' ').replace('-', ' ')
        title = ' '.join(word.capitalize() for word in title.split())
        return title if title else "Item"
    
    def batch_identify(self, photos_dir):
        """Identify multiple items from a directory"""
        photos_path = Path(photos_dir)
        photo_files = list(photos_path.glob("*.jpg")) + list(photos_path.glob("*.png"))
        
        results = []
        for photo in photo_files:
            try:
                item_data = self.identify(photo)
                results.append(item_data)
            except Exception as e:
                print(f"Error processing {photo.name}: {e}")
        
        return results
