#!/usr/bin/env python3
"""
Test script for Teams meetings functionality
"""

import os
import requests
from datetime import datetime, timedelta

def test_teams_meetings():
    """Test Teams meetings endpoints"""
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Teams Meetings Functionality")
    print("=" * 50)
    
    # Test 1: Check if Teams is authenticated
    print("\n1. Checking Teams authentication status...")
    try:
        response = requests.get(f"{base_url}/teams/status")
        if response.status_code == 200:
            data = response.json()
            if data.get("is_authenticated"):
                print("✅ Teams is authenticated")
            else:
                print("❌ Teams is not authenticated")
                return
        else:
            print(f"❌ Failed to check Teams status: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error checking Teams status: {e}")
        return
    
    # Test 2: Get meetings
    print("\n2. Fetching meetings...")
    try:
        response = requests.get(f"{base_url}/teams/meetings")
        if response.status_code == 200:
            meetings = response.json()
            print(f"✅ Found {len(meetings)} meetings")
            
            if meetings:
                print("\n📅 Recent meetings:")
                for i, meeting in enumerate(meetings[:3], 1):
                    start_time = meeting.get("start", "Unknown")
                    if start_time and "T" in start_time:
                        try:
                            dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                            formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            formatted_time = start_time
                    else:
                        formatted_time = start_time
                    
                    print(f"  {i}. {meeting.get('subject', 'No Subject')}")
                    print(f"     Start: {formatted_time}")
                    print(f"     Organizer: {meeting.get('organizer', 'Unknown')}")
                    print(f"     Online: {meeting.get('isOnlineMeeting', False)}")
                    if meeting.get("joinUrl"):
                        print(f"     Join URL: {meeting['joinUrl']}")
                    print()
        else:
            print(f"❌ Failed to get meetings: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting meetings: {e}")
    
    # Test 3: Get AI summary with meetings
    print("\n3. Getting AI summary with meetings...")
    try:
        response = requests.get(f"{base_url}/teams/ai-summary")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ AI summary generated")
            print(f"   Total Teams: {data.get('total_teams', 0)}")
            print(f"   Total Channels: {data.get('total_channels', 0)}")
            print(f"   Total Messages: {data.get('total_messages', 0)}")
            print(f"   Total Meetings: {data.get('total_meetings', 0)}")
            
            # Show a snippet of the summary
            summary = data.get('summary', '')
            if summary:
                lines = summary.split('\n')
                print(f"\n📋 Summary snippet (first 5 lines):")
                for line in lines[:5]:
                    if line.strip():
                        print(f"   {line}")
        else:
            print(f"❌ Failed to get AI summary: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error getting AI summary: {e}")
    
    # Test 4: Test chatbot with meetings
    print("\n4. Testing Teams chatbot with meetings...")
    try:
        response = requests.post(
            f"{base_url}/teams-chatbot/chat",
            json={"message": "What meetings do I have coming up?"}
        )
        if response.status_code == 200:
            data = response.json()
            print("✅ Chatbot response received")
            print(f"Response: {data.get('response', 'No response')[:200]}...")
        else:
            print(f"❌ Failed to get chatbot response: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing chatbot: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Teams meetings testing completed!")

if __name__ == "__main__":
    test_teams_meetings() 