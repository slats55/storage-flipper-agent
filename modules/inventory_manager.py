"""
Inventory Manager Module
Tracks items in Google Sheets or local database
"""

import json
import csv
from pathlib import Path
from datetime import datetime
import random
import string


class InventoryManager:
    """Manage inventory tracking and analytics"""
    
    def __init__(self, data_dir=None):
        if data_dir:
            self.data_dir = Path(data_dir)
        else:
            self.data_dir = Path.home() / "storage-flipper-agent" / "data" / "inventory"
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.inventory_file = self.data_dir / "inventory.csv"
        self._init_inventory_file()
    
    def _init_inventory_file(self):
        """Initialize inventory CSV if it doesn't exist"""
        if not self.inventory_file.exists():
            headers = [
                'sku', 'title', 'brand', 'category', 'condition',
                'cost', 'suggested_price', 'listed_price',
                'ebay_listed', 'facebook_listed', 'mercari_listed', 'offerup_listed',
                'sold', 'sold_platform', 'sold_price', 'sold_date',
                'date_acquired', 'date_listed', 'days_on_market',
                'photo_path', 'notes'
            ]
            
            with open(self.inventory_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
    
    def generate_sku(self):
        """Generate unique SKU"""
        # Format: YYYYMMDD-XXXX
        date_part = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f"{date_part}-{random_part}"
    
    def add_item(self, item_data, listings=None):
        """Add item to inventory"""
        sku = self.generate_sku()
        item_data['sku'] = sku
        
        # Prepare inventory record
        record = {
            'sku': sku,
            'title': item_data.get('title', ''),
            'brand': item_data.get('brand', ''),
            'category': item_data.get('category', ''),
            'condition': item_data.get('condition', ''),
            'cost': 0,  # Can be updated later
            'suggested_price': item_data.get('suggested_price', 0),
            'listed_price': item_data.get('suggested_price', 0),
            'ebay_listed': 'Yes' if listings and 'ebay' in listings else 'No',
            'facebook_listed': 'Yes' if listings and 'facebook' in listings else 'No',
            'mercari_listed': 'Yes' if listings and 'mercari' in listings else 'No',
            'offerup_listed': 'Yes' if listings and 'offerup' in listings else 'No',
            'sold': 'No',
            'sold_platform': '',
            'sold_price': 0,
            'sold_date': '',
            'date_acquired': datetime.now().strftime('%Y-%m-%d'),
            'date_listed': datetime.now().strftime('%Y-%m-%d'),
            'days_on_market': 0,
            'photo_path': item_data.get('photo_path', ''),
            'notes': ''
        }
        
        # Append to CSV
        with open(self.inventory_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=record.keys())
            writer.writerow(record)
        
        # Save detailed JSON record
        json_file = self.data_dir / f"{sku}.json"
        detailed_record = {
            **item_data,
            'listings': listings,
            'inventory_record': record
        }
        
        with open(json_file, 'w') as f:
            json.dump(detailed_record, f, indent=2)
        
        return sku
    
    def mark_sold(self, sku, platform, sold_price):
        """Mark an item as sold"""
        # Read inventory
        items = []
        with open(self.inventory_file, 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)
        
        # Update the sold item
        for item in items:
            if item['sku'] == sku:
                item['sold'] = 'Yes'
                item['sold_platform'] = platform
                item['sold_price'] = sold_price
                item['sold_date'] = datetime.now().strftime('%Y-%m-%d')
                break
        
        # Write back
        if items:
            with open(self.inventory_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=items[0].keys())
                writer.writeheader()
                writer.writerows(items)
        
        print(f"   ✅ Marked {sku} as sold on {platform} for ${sold_price}")
    
    def get_analytics(self):
        """Get inventory analytics"""
        with open(self.inventory_file, 'r') as f:
            reader = csv.DictReader(f)
            items = list(reader)
        
        total_items = len(items)
        sold_items = sum(1 for item in items if item['sold'] == 'Yes')
        unsold_items = total_items - sold_items
        
        total_value = sum(float(item['suggested_price'] or 0) for item in items if item['sold'] == 'No')
        total_revenue = sum(float(item['sold_price'] or 0) for item in items if item['sold'] == 'Yes')
        
        return {
            'total_items': total_items,
            'sold_items': sold_items,
            'unsold_items': unsold_items,
            'total_inventory_value': total_value,
            'total_revenue': total_revenue,
            'sell_through_rate': (sold_items / total_items * 100) if total_items > 0 else 0
        }
