#!/usr/bin/env python3
"""
Test script to demonstrate peril keyword combinations (single only).
"""

import json
import itertools
from typing import List

def load_peril_keywords() -> List[str]:
    """Load peril keywords from JSON file."""
    try:
        with open('peril_keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('peril_keywords', [])
    except FileNotFoundError:
        print("Warning: peril_keywords.json not found, using default keywords")
        return ["explosion damage", "lightning damage", "flood damage", "freezing damage", 
                "tornado damage", "storm damage", "hail damage", "pipe burst damage", 
                "structure damage", "water damage", "smoke damage"]

def generate_search_combinations() -> List[str]:
    """Generate single search combinations: state + keyword."""
    # Sample states for demonstration
    sample_states = ["Texas", "California", "Florida"]
    
    combinations = []
    
    # Single keyword combinations only
    for state in sample_states:
        for keyword in PERIL_KEYWORDS:
            combinations.append(f"{state} {keyword}")
    
    return combinations

if __name__ == "__main__":
    # Load peril keywords
    PERIL_KEYWORDS = load_peril_keywords()
    
    print("=== Peril Keywords ===")
    for i, keyword in enumerate(PERIL_KEYWORDS, 1):
        print(f"{i:2d}. {keyword}")
    
    print(f"\nTotal keywords: {len(PERIL_KEYWORDS)}")
    
    # Generate combinations
    combinations = generate_search_combinations()
    
    print(f"\n=== Sample Search Combinations ===")
    print(f"Total combinations generated: {len(combinations)}")
    
    # Show some examples
    print("\nSingle keyword examples:")
    for i, combo in enumerate(combinations[:6], 1):
        print(f"{i:2d}. {combo}")
    
    # Calculate total combinations for all states
    all_states = ["Arizona", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
                  "Idaho", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
                  "Maryland", "Michigan", "Minnesota", "Mississippi", "Montana", "Nebraska",
                  "Nevada", "New Hampshire", "New Jersey", "New Mexico", "North Carolina",
                  "North Dakota", "Ohio", "Oklahoma", "Oregon", "South Carolina", "Tennessee",
                  "Texas", "US Virgin Islands", "Utah", "Vermont", "Virginia", "Washington",
                  "West Virginia", "Wisconsin", "Wyoming", "DC"]
    
    total_single = len(all_states) * len(PERIL_KEYWORDS)
    
    print(f"\n=== Total Combinations for All States ===")
    print(f"Single keyword combinations: {total_single:,}")
    print(f"Total combinations: {total_single:,}")
