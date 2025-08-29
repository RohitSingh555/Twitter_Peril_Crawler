#!/usr/bin/env python3
"""
Excel Deduplication Script
==========================
Removes rows with duplicate or very similar content from Excel files.
Keeps the first occurrence and removes subsequent duplicates.

Usage:
    python deduplicate_excel.py [excel_file_path]
    
If no file path is provided, it will look for the most recent Excel file in the output folder.
"""

import os
import sys
import glob
import pandas as pd
from difflib import SequenceMatcher
from datetime import datetime

def find_latest_excel_file(output_dir="output"):
    """Find the most recent Excel file in the output directory."""
    pattern = os.path.join(output_dir, "*.xlsx")
    excel_files = glob.glob(pattern)
    
    if not excel_files:
        print(f"❌ No Excel files found in {output_dir}")
        return None
    
    # Sort by modification time and get the latest
    latest_file = max(excel_files, key=os.path.getmtime)
    print(f"📁 Found latest Excel file: {latest_file}")
    return latest_file

def is_similar(text1, text2, threshold=0.8):
    """Check if two texts are similar based on similarity threshold."""
    if pd.isna(text1) or pd.isna(text2):
        return False
    
    text1_str = str(text1).lower().strip()
    text2_str = str(text2).lower().strip()
    
    # If exact match (after cleaning), definitely duplicate
    if text1_str == text2_str:
        return True
    
    # Check for high similarity using SequenceMatcher
    similarity = SequenceMatcher(None, text1_str, text2_str).ratio()
    return similarity >= threshold

def remove_duplicate_content(excel_path, similarity_threshold=0.8):
    """Remove rows with duplicate or very similar content from Excel file."""
    try:
        print(f"🔍 Reading Excel file: {excel_path}")
        df = pd.read_excel(excel_path)
        original_count = len(df)
        
        if original_count <= 1:
            print(f"📊 No duplicates to remove (only {original_count} row)")
            return
        
        print(f"📊 Checking {original_count} rows for duplicates...")
        print(f"🎯 Similarity threshold: {similarity_threshold}")
        
        # Find and remove duplicates
        rows_to_drop = []
        
        for i in range(len(df)):
            if i in rows_to_drop:
                continue
                
            current_content = df.iloc[i]['content']
            
            for j in range(i + 1, len(df)):
                if j in rows_to_drop:
                    continue
                    
                compare_content = df.iloc[j]['content']
                
                if is_similar(current_content, compare_content, similarity_threshold):
                    # Keep the first occurrence, mark the second for removal
                    rows_to_drop.append(j)
                    print(f"🔄 Found duplicate: Row {j+1} similar to Row {i+1}")
        
        # Remove duplicate rows
        if rows_to_drop:
            df_cleaned = df.drop(df.index[rows_to_drop])
            df_cleaned = df_cleaned.reset_index(drop=True)
            
            # Save the cleaned data back to Excel (overwrites original)
            df_cleaned.to_excel(excel_path, index=False)
            
            removed_count = original_count - len(df_cleaned)
            print(f"✅ Removed {removed_count} duplicate rows")
            print(f"📊 Final count: {len(df_cleaned)} rows")
            print(f"💾 Cleaned file saved: {excel_path}")
            
        else:
            print(f"✅ No duplicates found")
            
    except Exception as e:
        print(f"❌ Error removing duplicates: {e}")
        return False
    
    return True

def main():
    """Main execution function"""
    print("🧹 Excel Deduplication Tool")
    print("=" * 50)
    
    # Determine input file
    if len(sys.argv) > 1:
        excel_path = sys.argv[1]
        if not os.path.exists(excel_path):
            print(f"❌ File not found: {excel_path}")
            return
    else:
        # Look for most recent Excel file in output folder
        excel_path = find_latest_excel_file()
        if not excel_path:
            print("❌ No Excel files found. Please specify a file path or ensure output folder contains Excel files.")
            return
    
    print(f"📁 Processing file: {excel_path}")
    
    # Get similarity threshold from user
    try:
        threshold_input = input("🎯 Enter similarity threshold (0.0-1.0, default 0.8): ").strip()
        if threshold_input:
            similarity_threshold = float(threshold_input)
            if not 0.0 <= similarity_threshold <= 1.0:
                print("⚠️  Invalid threshold, using default 0.8")
                similarity_threshold = 0.8
        else:
            similarity_threshold = 0.8
    except ValueError:
        print("⚠️  Invalid threshold, using default 0.8")
        similarity_threshold = 0.8
    
    print(f"🎯 Using similarity threshold: {similarity_threshold}")
    
    # Run deduplication
    print("\n🚀 Starting deduplication process...")
    success = remove_duplicate_content(excel_path, similarity_threshold)
    
    if success:
        print("\n🎉 Deduplication completed successfully!")
    else:
        print("\n❌ Deduplication failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
