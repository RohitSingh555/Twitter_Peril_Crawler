#!/usr/bin/env python3
"""
Script to extract data from the latest Excel file and send it to the API
without sending any emails.
"""

import os
import glob
import pandas as pd
import json
from datetime import datetime
from utils import send_to_api

def find_latest_excel_file(output_dir="output"):
    """
    Find the most recent Excel file in the output directory.
    
    Args:
        output_dir (str): Directory to search for Excel files
        
    Returns:
        str: Path to the latest Excel file, or None if not found
    """
    # Pattern to match verified_fires Excel files
    pattern = os.path.join(output_dir, "verified_fires_*.xlsx")
    excel_files = glob.glob(pattern)
    
    if not excel_files:
        print(f"[ERROR] No Excel files found in {output_dir}")
        return None
    
    # Sort by modification time and get the latest
    latest_file = max(excel_files, key=os.path.getmtime)
    print(f"[INFO] Found latest Excel file: {latest_file}")
    return latest_file

def excel_to_json_data(excel_path):
    """
    Convert Excel data to the format expected by the API.
    
    Args:
        excel_path (str): Path to the Excel file
        
    Returns:
        list: List of dictionaries in the API format
    """
    try:
        # Read Excel file
        df = pd.read_excel(excel_path)
        print(f"[INFO] Loaded {len(df)} records from Excel file")
        
        # Convert DataFrame to list of dictionaries
        api_data = []
        
        for index, row in df.iterrows():
            # Convert row to dictionary
            item = row.to_dict()
            
            # Handle the published_date - it might already be in ISO format
            raw_published_date = item.get("published_date", "")
            if raw_published_date:
                # Check if it's already in ISO format (contains 'T' and timezone info)
                if 'T' in str(raw_published_date) and ('+' in str(raw_published_date) or 'Z' in str(raw_published_date)):
                    parsed_published_date = str(raw_published_date)
                else:
                    # Use as is if not in ISO format
                    parsed_published_date = str(raw_published_date)
            else:
                parsed_published_date = datetime.now().isoformat()
            
            # Handle NaN values properly - convert to empty string if NaN
            def clean_value(value):
                if pd.isna(value) or str(value).lower() == 'nan':
                    return ""
                return str(value)
            
            # Ensure all required fields are present with proper types
            api_item = {
                "title": clean_value(item.get("title", "")),
                "content": clean_value(item.get("content", "")),
                "published_date": parsed_published_date,
                "url": clean_value(item.get("url", "")),
                "source": clean_value(item.get("source", "")),
                "fire_related_score": float(item.get("fire_related_score", 0.8)),
                "verification_result": clean_value(item.get("verification_result", "yes")),
                "verified_at": clean_value(item.get("verified_at", datetime.now().isoformat())),
                "state": clean_value(item.get("state", "")),  # Use extracted state from AI
                "county": clean_value(item.get("county", "")),  # Use extracted county from AI
                "city": "",  # Could be extracted from content if needed
                "province": clean_value(item.get("province", "")),  # Could be extracted from content if needed
                "country": "USA",  # Default country
                "latitude": 0.0,  # Default to 0.0 instead of None
                "longitude": 0.0,  # Default to 0.0 instead of None
                "image_url": clean_value(item.get("image_url", "")),  # Could be extracted from content if needed
                "tags": "fire,emergency,news,twitter",  # Default tags
                "reporter_name": "Twitter Fire Detection Bot"  # Could be extracted from content if needed
            }
            
            api_data.append(api_item)
        
        print(f"[INFO] Converted {len(api_data)} records to API format")
        return api_data
        
    except Exception as e:
        print(f"[ERROR] Error reading Excel file: {e}")
        return []

def save_temp_json(api_data, output_dir="output"):
    """
    Save the API data to a temporary JSON file.
    
    Args:
        api_data (list): List of dictionaries in API format
        output_dir (str): Directory to save the JSON file
        
    Returns:
        str: Path to the saved JSON file
    """
    try:
        # Create timestamped filename
        dt_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_filename = f"temp_api_data_{dt_str}.json"
        json_path = os.path.join(output_dir, json_filename)
        
        # Save to JSON file
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(api_data, f, ensure_ascii=False, indent=2)
        
        print(f"[INFO] Saved temporary JSON file: {json_path}")
        return json_path
        
    except Exception as e:
        print(f"[ERROR] Error saving JSON file: {e}")
        return None

def send_excel_data_to_api(excel_path):
    """
    Send Excel data to the API.
    
    Args:
        excel_path (str): Path to the Excel file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"[START] Processing Excel file: {excel_path}")
        
        # Convert Excel to API format
        api_data = excel_to_json_data(excel_path)
        
        if not api_data:
            print("[ERROR] No data to send to API")
            return False
        
        # Save to temporary JSON file
        json_path = save_temp_json(api_data)
        
        if not json_path:
            print("[ERROR] Failed to create temporary JSON file")
            return False
        
        # Send to API
        print(f"[API] Sending {len(api_data)} records to API...")
        success = send_to_api(json_path, len(api_data))
        
        if success:
            print(f"[SUCCESS] Successfully sent {len(api_data)} records to API")
        else:
            print(f"[ERROR] Failed to send data to API")
        
        # Clean up temporary JSON file
        try:
            os.remove(json_path)
            print(f"[CLEANUP] Removed temporary file: {json_path}")
        except Exception as e:
            print(f"[WARNING] Could not remove temporary file: {e}")
        
        return success
        
    except Exception as e:
        print(f"[ERROR] Error in send_excel_data_to_api: {e}")
        return False

def main():
    """
    Main function to find latest Excel file and send to API.
    """
    print("🔥 Excel to API Sender")
    print("=" * 50)
    
    # Find the latest Excel file
    latest_excel = find_latest_excel_file()
    
    if not latest_excel:
        print("[ERROR] No Excel files found. Please run the fire detection system first.")
        return
    
    # Send data to API
    success = send_excel_data_to_api(latest_excel)
    
    if success:
        print("\n✅ Process completed successfully!")
    else:
        print("\n❌ Process failed. Check the logs above for details.")

if __name__ == "__main__":
    main() 