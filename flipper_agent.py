#!/usr/bin/env python3
"""
Storage Unit Flipper Agent
Main orchestration script for automating storage unit flipping workflow
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from tqdm import tqdm

# Project root on path so ``modules.*`` imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent))

from modules.agent_logging import configure_logging
from modules.inventory_manager import InventoryManager
from modules.item_identifier import ItemIdentifier
from modules.listing_generator import ListingGenerator
from modules.price_researcher import PriceResearcher

logger = logging.getLogger("flipper.flipper_agent")


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

        logger.info("process_item start photo_path=%s", photo_path)

        print("🔍 Step 1: Identifying item...")
        item_data = self.identifier.identify(photo_path)
        print(f"   Found: {item_data.get('title', 'Unknown item')}")

        print("\n💰 Step 2: Researching market prices...")
        pricing_data = self.researcher.research(item_data)
        item_data.update(pricing_data)
        print(f"   Suggested price: ${item_data.get('suggested_price', 0):.2f}")

        print("\n📝 Step 3: Generating listings...")
        try:
            listings = self.listing_gen.generate(item_data)
        except Exception as exc:
            logger.exception("Listing generation failed: %s", exc)
            listings = {}
        print(f"   Created {len(listings)} platform-specific listings")

        print("\n📊 Step 4: Adding to inventory...")
        try:
            self.inventory.add_item(item_data, listings)
        except OSError as exc:
            logger.exception("Inventory write failed: %s", exc)
            raise
        print(f"   SKU: {item_data.get('sku', 'N/A')}")

        print(f"\n{'='*60}")
        print("✅ Item processing complete!")
        print(f"{'='*60}\n")

        logger.info("process_item complete sku=%s", item_data.get("sku"))
        return item_data

    def process_batch(self, photos_dir):
        """Process multiple items from a directory"""
        photos_path = Path(photos_dir)
        photo_files = (
            list(photos_path.glob("*.jpg"))
            + list(photos_path.glob("*.png"))
            + list(photos_path.glob("*.jpeg"))
        )

        print(f"\n🚀 BATCH PROCESSING: {len(photo_files)} items\n")
        logger.info("process_batch dir=%s count=%s", photos_dir, len(photo_files))

        results = []
        failures = 0
        for photo in tqdm(photo_files, desc="Items", unit="item"):
            print(f"\n[{photo.name}]")
            try:
                result = self.process_item(str(photo))
                results.append(result)
            except Exception as exc:
                failures += 1
                logger.exception("Batch item failed path=%s: %s", photo, exc)
                print(f"❌ Error processing {photo.name}: {exc}")

        print(f"\n{'='*60}")
        print(f"BATCH COMPLETE: {len(results)}/{len(photo_files)} successful")
        if failures:
            logger.warning("Batch failures=%s success=%s", failures, len(results))
        print(f"{'='*60}")

        total_value = sum(r.get("suggested_price", 0) for r in results)
        print(f"\nEstimated total value: ${total_value:.2f}")

        return results


def main():
    configure_logging()
    parser = argparse.ArgumentParser(description="Storage Unit Flipper Agent")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    batch_parser = subparsers.add_parser("process-batch", help="Process multiple items")
    batch_parser.add_argument("photos_dir", help="Directory containing item photos")

    single_parser = subparsers.add_parser("process-item", help="Process single item")
    single_parser.add_argument("photo", help="Path to item photo")

    id_parser = subparsers.add_parser("identify-item", help="Identify item from photo")
    id_parser.add_argument("photo", help="Path to item photo")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    agent = FlipperAgent()

    if args.command == "process-batch":
        agent.process_batch(args.photos_dir)
    elif args.command == "process-item":
        agent.process_item(args.photo)
    elif args.command == "identify-item":
        result = agent.identifier.identify(args.photo)
        print(f"\nIdentified: {result.get('title', 'Unknown')}")
        print(f"Category: {result.get('category', 'Unknown')}")
        print(f"Condition: {result.get('condition', 'Unknown')}")


if __name__ == "__main__":
    main()
