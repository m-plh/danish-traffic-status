#!/usr/bin/env python3
"""
Test script for Danish Traffic Status APIs.
This script tests the connection to the DSB and Metro APIs used by the component.
"""
import argparse
import json
import sys
from datetime import datetime
import requests


def test_train_api():
    """Test the DSB train status API."""
    print("Testing DSB train status API...")
    
    base_url = "https://www.dsb.dk/api/travelplans/gettrafficinfolist?lang=da"
    
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not isinstance(data, list):
            print("Error: Unexpected response format. Expected a list.")
            return False
        
        print(f"Success! Received {len(data)} messages from the DSB API.")
        
        # Filter active messages for S-trains
        now = datetime.now()
        active_messages = [
            msg for msg in data
            if msg.get("sender") == "S-tog" and
            datetime.fromisoformat(msg.get("validFromDate").replace("Z", "+00:00")) <= now and
            (not msg.get("validToDate") or 
             datetime.fromisoformat(msg.get("validToDate").replace("Z", "+00:00")) >= now)
        ]
        
        print(f"Found {len(active_messages)} active messages for S-trains.")
        
        if active_messages:
            print("\nExample message:")
            message = active_messages[0]
            print(f"  Header: {message.get('header')}")
            print(f"  Body: {message.get('body')[:100]}...")
            print(f"  Urgent: {message.get('urgent', False)}")
            print(f"  URL: {message.get('url', 'N/A')}")
        
        return True
        
    except Exception as err:
        print(f"Error connecting to DSB API: {err}")
        return False


def test_metro_api():
    """Test the Metro status API."""
    print("\nTesting Metro status API...")
    
    base_url = "https://metroselskabet.euwest01.umbraco.io/api/operationData/GetOperationData/"
    
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not isinstance(data, dict) or "activeMessages" not in data:
            print("Error: Unexpected response format. Expected a dictionary with 'activeMessages'.")
            return False
        
        active_messages = data.get("activeMessages", [])
        print(f"Success! Received {len(active_messages)} active messages from the Metro API.")
        
        if active_messages:
            print("\nExample message:")
            message = active_messages[0]
            print(f"  Name: {message.get('name')}")
            print(f"  Type: {message.get('Type')}")
            print(f"  Line Group: {message.get('lineSetup', {}).get('lineGroup')}")
            print(f"  Is Clear Message: {message.get('isClearMessage', False)}")
        
        return True
        
    except Exception as err:
        print(f"Error connecting to Metro API: {err}")
        return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test Danish Traffic Status APIs")
    parser.add_argument("--train", action="store_true", help="Test only the train API")
    parser.add_argument("--metro", action="store_true", help="Test only the metro API")
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    success = True
    
    if args.train or not (args.train or args.metro):
        train_success = test_train_api()
        success = success and train_success
    
    if args.metro or not (args.train or args.metro):
        metro_success = test_metro_api()
        success = success and metro_success
    
    print("\nTest Summary:")
    if success:
        print("✅ All tests passed! The APIs are accessible.")
        print("You should be able to use the Danish Traffic Status component.")
    else:
        print("❌ Some tests failed. Please check your network connection and try again.")
        print("If the problem persists, the APIs might be temporarily unavailable.")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
