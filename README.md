# World of Warcraft Gacha System Simulator

A Python-based gacha system simulator using World of Warcraft items to test and analyze gacha mechanics and drop rates.

## Features

- **Rarity Tiers:**
  - Mythic (0.1%)
  - SSR (3%)
  - SR (16%)
  - R (80.9%)

- **Pity Systems:**
  - Soft pity for SSR starts at 75 pulls
  - Hard pity SSR guarantee at 110 pulls
  - Soft pity for Mythic starts at 800 pulls
  - Hard pity Mythic guarantee at 5000 pulls

- **Game Items:**
  - Iconic World of Warcraft items divided by rarity tiers
  - Includes legendary weapons, mounts, and consumables

## How to Use

1. Run the script:
```bash
python teste.py
```

2. Available options:
   - Single Pull: Draw one item
   - Multi Pull: Draw multiple items (1-10000)
   - View Stats: Check your pull statistics and inventory
   - Change Player: Switch to a different player profile
   - Exit: Close the program

## Statistics Tracking

The system tracks:
- Total pulls per player
- Item inventory by rarity
- Pull history
- Drop rates statistics
- Pity counter status

## Technical Details

- Written in Python 3
- Uses built-in random module for gacha mechanics
- Implements both soft and hard pity systems
- Maintains persistent player statistics during session
