#!/usr/bin/env python3
"""
Storage Unit Flipper Agent
Main orchestration script for automating storage unit flipping workflow
"""

import sys
import argparse
from pathlib import Path

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules"))

from item_identifier import ItemIdentifier
from price_researcher import PriceResearcher
from listing_generator import ListingGenerator
from inventory_manager import InventoryManager


class FlipperAgent:
    """Main agent orchestrator"""
    
    def __init__(self):
        self.identifier = ItemIdentifier()
        self.researcher = PriceResearcher()
        self.listing_gen = ListingGenerator()
        self.inventory = InventoryManager()
    
    def process_item(self, photo_path):
        """Complete workflow for a single item"""
        print(f"\n{'='*60}")
        print(f"Processing: {photo_path}")
        print(f"{'='*60}\n")
        
        # Step 1: Identify item from photo
        print("🔍 Step 1: Identifying item...")
        item_data = self.identifier.identify(photo_path)
        print(f"   Found: {item_data.get('title', 'Unknown item')}")
        
        # Step 2: Research pricing
        print("\n💰 Step 2: Researching market prices...")
        pricing_data = self.researcher.research(item_data)
        item_data.update(pricing_data)
        print(f"   Suggested price: ${item_data.get('suggested_price', 0):.2f}")
        
        # Step 3: Generate listings
        print("\n📝 Step 3: Generating listings...")
        listings = self.listing_gen.generate(item_data)
        print(f"   Created {len(listings)} platform-specific listings")
        
        # Step 4: Add to inventory
        print("\n📊 Step 4: Adding to inventory...")
        self.inventory.add_item(item_data, listings)
        print(f"   SKU: {item_data.get('sku', 'N/A')}")
        
        print(f"\n{'='*60}")
        print("✅ Item processing complete!")
        print(f"{'='*60}\n")
        
        return item_data
    
    def process_batch(self, photos_dir):
        """Process multiple items from a directory"""
        photos_path = Path(photos_dir)
        photo_files = list(photos_path.glob("*.jpg")) + list(photos_path.glob("*.png"))
        
        print(f"\n🚀 BATCH PROCESSING: {len(photo_files)} items\n")
        
        results = []
        for i, photo in enumerate(photo_files, 1):
            print(f"\n[{i}/{len(photo_files)}]")
            try:
                result = self.process_item(str(photo))
                results.append(result)
            except Exception as e:
                print(f"❌ Error processing {photo.name}: {e}")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"BATCH COMPLETE: {len(results)}/{len(photo_files)} successful")
        print(f"{'='*60}")
        
        total_value = sum(r.get('suggested_price', 0) for r in results)
        print(f"\nEstimated total value: ${total_value:.2f}")
        
        return results


def main():
    parser = argparse.ArgumentParser(description="Storage Unit Flipper Agent")
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Process batch command
    batch_parser = subparsers.add_parser('process-batch', help='Process multiple items')
    batch_parser.add_argument('photos_dir', help='Directory containing item photos')
    
    # Process single item
    single_parser = subparsers.add_parser('process-item', help='Process single item')
    single_parser.add_argument('photo', help='Path to item photo')
    
    # Identify only
    id_parser = subparsers.add_parser('identify-item', help='Identify item from photo')
    id_parser.add_argument('photo', help='Path to item photo')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    agent = FlipperAgent()
    
    if args.command == 'process-batch':
        agent.process_batch(args.photos_dir)
    elif args.command == 'process-item':
        agent.process_item(args.photo)
    elif args.command == 'identify-item':
        result = agent.identifier.identify(args.photo)
        print(f"\nIdentified: {result.get('title', 'Unknown')}")
        print(f"Category: {result.get('category', 'Unknown')}")
        print(f"Condition: {result.get('condition', 'Unknown')}")


if __name__ == "__main__":
    main()
