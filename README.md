# Storage Unit Flipper Agent

AI-powered automation for storage unit flipping businesses.

## Problem
Storage unit flippers spend 40-80 hours per unit on manual tasks:
- Identifying items and brands (5-15 min per item × 200-500 items)
- Researching market prices across platforms
- Writing listings and taking photos
- Posting to multiple platforms separately
- Tracking inventory

## Solution
AI agent that reduces processing time to 17-25 hours (57-68% savings)

## MVP Features

### 1. Item Identification & Pricing
- Upload photos of items
- AI identifies product, brand, model, condition
- Auto-research comparable prices on eBay, Facebook Marketplace
- Generate pricing recommendations

### 2. Listing Generation
- Create SEO-optimized titles
- Write compelling descriptions
- Format for multiple platforms
- Suggest categories

### 3. Multi-Platform Management
- Post to eBay, Facebook Marketplace, Mercari, OfferUp
- Track where each item is listed
- Sync inventory across platforms

### 4. Inventory Tracking
- Google Sheets integration
- SKU generation
- Location tracking
- Days-on-market monitoring
- Profit/loss analytics

### 5. Analytics & Reporting
- Revenue tracking
- Best-selling categories
- Time-to-sale metrics

## Tech Stack
- Hermes Agent (orchestration)
- Vision AI (item identification)
- Web scraping (price research)
- Google Sheets API (inventory)
- Platform APIs (eBay, Facebook, etc.)

## Workflow
```
1. User uploads photos → 2. AI identifies items → 3. AI researches prices → 
4. AI generates listings → 5. User reviews/approves → 6. AI posts to platforms → 
7. Auto-tracks inventory → 8. Reports analytics
```

## Getting Started

### Installation
```bash
cd ~/storage-flipper-agent
pip install -r requirements.txt
```

### Configuration
1. Copy `.env.example` to `.env`
2. Add your API keys
3. Configure Google Sheets access

### Usage
```bash
# Process a batch of item photos
python flipper_agent.py process-batch photos/

# Single item workflow
python flipper_agent.py identify-item photo.jpg
python flipper_agent.py research-price "Brand Name Product"
python flipper_agent.py generate-listing item_data.json
```

## Project Status
- [ ] Core architecture
- [ ] Item identification module
- [ ] Price research module
- [ ] Listing generator
- [ ] Platform integrations
- [ ] Inventory system
- [ ] Testing with real data
