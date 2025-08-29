#!/usr/bin/env python3
"""
Test runner script for the Twitter Peril Crawler.
Run this script to execute all tests.
"""

import os
import sys

# Add parent directory to path so we can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_combinations():
    """Run the test combinations script."""
    print("=== Running Test Combinations ===")
    try:
        # Run the test combinations script directly
        import subprocess
        result = subprocess.run([sys.executable, "test/test_combinations.py"], 
                              capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(__file__)))
        if result.returncode == 0:
            print(result.stdout)
            print("✅ Test combinations completed successfully")
            return True
        else:
            print(f"❌ Test combinations failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Test combinations failed: {e}")
        return False

def run_peril_search_test():
    """Test the peril search functionality."""
    print("\n=== Testing Peril Search ===")
    try:
        from tweet_peril_search import get_all_peril_search_combinations, load_peril_keywords
        
        # Test loading keywords
        keywords = load_peril_keywords()
        print(f"✅ Loaded {len(keywords)} peril keywords")
        
        # Test generating combinations
        combinations = get_all_peril_search_combinations()
        print(f"✅ Generated {len(combinations):,} search combinations")
        
        # Show a few examples
        print("Sample combinations:")
        for i, combo in enumerate(combinations[:5], 1):
            print(f"  {i}. {combo}")
        
        print("✅ Peril search test completed successfully")
        return True
    except Exception as e:
        print(f"❌ Peril search test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Twitter Peril Crawler Tests\n")
    
    success_count = 0
    total_tests = 2
    
    # Run test combinations
    if run_test_combinations():
        success_count += 1
    
    # Run peril search test
    if run_peril_search_test():
        success_count += 1
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Tests passed: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
