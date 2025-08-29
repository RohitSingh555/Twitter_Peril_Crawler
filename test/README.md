# Test Directory

This directory contains all test scripts for the Twitter Peril Crawler.

## Test Files

- **`test_combinations.py`** - Tests the peril keyword combinations and permutations
- **`run_tests.py`** - Main test runner that executes all tests

## Running Tests

### Run All Tests
```bash
python test/run_tests.py
```

### Run Individual Tests
```bash
# Test combinations only
python test/test_combinations.py

# Test peril search functionality
python -c "from tweet_peril_search import get_all_peril_search_combinations; print(len(get_all_peril_search_combinations()))"
```

## Test Coverage

The tests verify:
1. ✅ Loading peril keywords from JSON file
2. ✅ Generating search combinations (state + keyword)
3. ✅ Correct number of combinations (440 total)
4. ✅ Import and function availability

## Expected Output

When running `run_tests.py`, you should see:
- Peril keywords loaded (11 keywords)
- Search combinations generated (440 combinations)
- Sample combinations displayed
- All tests passing
