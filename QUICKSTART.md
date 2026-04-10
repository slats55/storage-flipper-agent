# Storage Flipper Agent - Quick Start Guide

## Installation

1. Navigate to the project directory:
   ```bash
   cd ~/storage-flipper-agent
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment (optional for MVP):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## Usage

### Run Demo
Test the agent with mock data:
```bash
python demo.py
```

### Process Single Item
```bash
python flipper_agent.py process-item path/to/photo.jpg
```

### Process Batch of Items
```bash
# Put photos in data/photos/
python flipper_agent.py process-batch data/photos/
```

### Workflow

1. **Take Photos**: Photograph items from storage unit
   - Clear, well-lit photos
   - Show brand names/model numbers
   - Capture any damage or defects

2. **Process Items**: Run the agent on your photos
   ```bash
   python flipper_agent.py process-batch data/photos/unit-042/
   ```

3. **Review Output**: Check generated listings in data/listings/
   - Verify item identification
   - Confirm pricing makes sense
   - Adjust descriptions if needed

4. **Post Listings**: 
   - Manual: Copy/paste to eBay, Facebook, etc.
   - Automated (future): Use platform APIs

5. **Track Sales**: Update inventory when items sell
   - SKU tracking in data/inventory/inventory.csv
   - Or integrate with Google Sheets

## Project Structure

```
storage-flipper-agent/
├── flipper_agent.py          # Main agent script
├── demo.py                   # Demo with mock data
├── modules/
│   ├── item_identifier.py    # Vision-based item ID
│   ├── price_researcher.py   # Market price research
│   ├── listing_generator.py  # Multi-platform listings
│   └── inventory_manager.py  # Inventory tracking
├── data/
│   ├── photos/              # Input: Item photos
│   ├── listings/            # Output: Generated listings
│   └── inventory/           # Database: inventory.csv
└── config/                  # Configuration files
```

## Next Steps

### MVP (Current)
- ✅ Item identification framework
- ✅ Price research structure
- ✅ Listing generation
- ✅ Basic inventory tracking

### Phase 2
- [ ] Integrate Hermes vision_analyze for real photo analysis
- [ ] Web scraping for live eBay pricing
- [ ] Google Sheets integration
- [ ] Batch photo processing

### Phase 3
- [ ] eBay API integration for automated posting
- [ ] Facebook Marketplace automation (where possible)
- [ ] Customer message handling
- [ ] Sales analytics dashboard

## Tips

1. **Photo Quality Matters**: Better photos = better AI identification
2. **Batch Processing**: Process 10-20 items at a time for efficiency
3. **Price Verification**: Always double-check AI pricing suggestions
4. **Test First**: Run demo and single items before batch processing
5. **Backup Data**: Keep photos and inventory.csv backed up

## Troubleshooting

**"Module not found" error**:
```bash
cd ~/storage-flipper-agent
python -m pip install -r requirements.txt
```

**No photos found**:
- Check photo extensions (.jpg, .png)
- Verify path to photos directory

**Pricing seems off**:
- Fallback pricing is used when web research fails
- Manually research first few items to calibrate

## Support

For issues or questions, check:
- README.md for project overview
- Module docstrings for technical details
- Hermes documentation for agent features
