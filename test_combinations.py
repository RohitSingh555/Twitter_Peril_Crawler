#!/usr/bin/env python3
"""
Test script to demonstrate damage keyword combinations and permutations.
"""

import json
import itertools
from typing import List

def load_damage_keywords() -> List[str]:
    """Load damage keywords from JSON file."""
    try:
        with open('damage_keywords.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('damage_keywords', [])
    except FileNotFoundError:
        print("Warning: damage_keywords.json not found, using default keywords")
        return ["explosion damage", "lightning damage", "flood damage", "freezing damage", 
                "tornado damage", "storm damage", "hail damage", "pipe burst damage", 
                "structure damage", "water damage", "smoke damage"]

def generate_search_combinations() -> List[str]:
    """Generate all possible search combinations using permutations and combinations of damage keywords."""
    # Sample states for demonstration
    sample_states = ["Texas", "California", "Florida"]
    
    combinations = []
    
    # Single keyword combinations
    for state in sample_states:
        for keyword in DAMAGE_KEYWORDS:
            combinations.append(f"{state} {keyword}")
    
    # Two keyword combinations (permutations)
    for state in sample_states:
        for combo in itertools.permutations(DAMAGE_KEYWORDS, 2):
            combinations.append(f"{state} {' '.join(combo)}")
    
    # Three keyword combinations (permutations)
    for state in sample_states:
        for combo in itertools.permutations(DAMAGE_KEYWORDS, 3):
            combinations.append(f"{state} {' '.join(combo)}")
    
    return combinations

if __name__ == "__main__":
    # Load damage keywords
    DAMAGE_KEYWORDS = load_damage_keywords()
    
    print("=== Damage Keywords ===")
    for i, keyword in enumerate(DAMAGE_KEYWORDS, 1):
        print(f"{i:2d}. {keyword}")
    
    print(f"\nTotal keywords: {len(DAMAGE_KEYWORDS)}")
    
    # Generate combinations
    combinations = generate_search_combinations()
    
    print(f"\n=== Sample Search Combinations ===")
    print(f"Total combinations generated: {len(combinations)}")
    
    # Show some examples
    print("\nSingle keyword examples:")
    for i, combo in enumerate(combinations[:6], 1):
        print(f"{i:2d}. {combo}")
    
    print("\nTwo keyword examples:")
    for i, combo in enumerate(combinations[len(DAMAGE_KEYWORDS)*3:len(DAMAGE_KEYWORDS)*3+6], 1):
        print(f"{i:2d}. {combo}")
    
    print("\nThree keyword examples:")
    for i, combo in enumerate(combinations[-6:], 1):
        print(f"{i:2d}. {combo}")
    
    # Calculate total combinations for all states
    all_states = ["Arizona", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
                  "Idaho", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
                  "Maryland", "Michigan", "Minnesota", "Mississippi", "Montana", "Nebraska",
                  "Nevada", "New Hampshire", "New Jersey", "New Mexico", "North Carolina",
                  "North Dakota", "Ohio", "Oklahoma", "Oregon", "South Carolina", "Tennessee",
                  "Texas", "US Virgin Islands", "Utah", "Vermont", "Virginia", "Washington",
                  "West Virginia", "Wisconsin", "Wyoming", "DC"]
    
    total_single = len(all_states) * len(DAMAGE_KEYWORDS)
    total_double = len(all_states) * len(list(itertools.permutations(DAMAGE_KEYWORDS, 2)))
    total_triple = len(all_states) * len(list(itertools.permutations(DAMAGE_KEYWORDS, 3)))
    total_all = total_single + total_double + total_triple
    
    print(f"\n=== Total Combinations for All States ===")
    print(f"Single keyword combinations: {total_single:,}")
    print(f"Two keyword combinations: {total_double:,}")
    print(f"Three keyword combinations: {total_triple:,}")
    print(f"Total combinations: {total_all:,}")
