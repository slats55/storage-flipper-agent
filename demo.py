#!/usr/bin/env python3
"""
Demo script to test the Storage Flipper Agent
"""

import logging
import sys
from pathlib import Path

# Project root on path so ``modules.*`` imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.agent_logging import configure_logging
from modules.item_identifier import ItemIdentifier

logger = logging.getLogger("flipper.demo")
from modules.price_researcher import PriceResearcher
from modules.listing_generator import ListingGenerator
from modules.inventory_manager import InventoryManager


def demo_single_item():
    """Demo processing a single item"""
    configure_logging()
    logger.info("demo_single_item started")

    print("\n" + "="*70)
    print(" STORAGE FLIPPER AGENT - DEMO")
    print("="*70)
    print("\nThis demo shows how the agent processes a single item.\n")
    
    # Create mock item data (in production, this comes from vision analysis)
    print("📸 Simulating photo analysis...")
    mock_item = {
        'photo_path': 'photos/vintage_camera.jpg',
        'title': 'Vintage Kodak Film Camera',
        'brand': 'Kodak',
        'model': 'Instamatic 104',
        'category': 'Collectibles',
        'condition': 'Good',
        'features': ['Working shutter', 'Clean lens', 'Original case included']
    }
    
    print(f"   ✓ Identified: {mock_item['title']}")
    print(f"   Brand: {mock_item['brand']}")
    print(f"   Condition: {mock_item['condition']}")
    
    # Research pricing
    print("\n💰 Researching market prices...")
    researcher = PriceResearcher()
    pricing_data = researcher.research(mock_item)
    mock_item.update(pricing_data)
    
    print(f"   ✓ Found {pricing_data['comp_count']} comparable sales")
    print(f"   Price range: ${pricing_data['price_range'][0]:.2f} - ${pricing_data['price_range'][1]:.2f}")
    print(f"   Suggested price: ${pricing_data['suggested_price']:.2f}")
    
    # Generate listings
    print("\n📝 Generating platform listings...")
    generator = ListingGenerator()
    listings = generator.generate(mock_item)
    
    print(f"\n   Preview - eBay Listing:")
    print(f"   Title: {listings['ebay']['title']}")
    print(f"   Price: ${listings['ebay']['price']:.2f}")
    print(f"   Description:\n   {listings['ebay']['description'][:150]}...")
    
    # Add to inventory
    print("\n📊 Adding to inventory system...")
    inventory = InventoryManager()
    sku = inventory.add_item(mock_item, listings)
    
    print(f"   ✓ SKU assigned: {sku}")
    print(f"   ✓ Saved to inventory database")
    
    # Show analytics
    print("\n📈 Current Inventory Analytics:")
    analytics = inventory.get_analytics()
    print(f"   Total items: {analytics['total_items']}")
    print(f"   Unsold items: {analytics['unsold_items']}")
    print(f"   Total inventory value: ${analytics['total_inventory_value']:.2f}")
    print(f"   Total revenue: ${analytics['total_revenue']:.2f}")
    
    print("\n" + "="*70)
    print(" ✅ DEMO COMPLETE")
    print("="*70)
    print("\nNext steps:")
    print("1. Take photos of actual items")
    print("2. Run: python flipper_agent.py process-item photo.jpg")
    print("3. Review generated listings")
    print("4. Post to platforms manually or via API")
    print("5. Track sales in inventory system\n")


def show_help():
    """Show available commands"""
    print("\nStorage Flipper Agent - Commands:\n")
    print("  python demo.py              Run demo with mock data")
    print("  python flipper_agent.py process-item photo.jpg")
    print("                              Process a single item photo")
    print("  python flipper_agent.py process-batch photos/")
    print("                              Process multiple items")
    print("  python flipper_agent.py identify-item photo.jpg")
    print("                              Just identify an item\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--help':
        show_help()
    else:
        demo_single_item()
