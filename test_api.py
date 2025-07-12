import requests
import os
from pathlib import Path

# Configuration
BASE_URL = "http://localhost:8000"

def test_upload_video():
    """Test video upload endpoint"""
    print("Testing video upload...")
    
    # Create a dummy video file for testing
    test_video_path = "test_video.mp4"
    
    # Create a small test file (1KB) that looks like a video
    with open(test_video_path, "wb") as f:
        f.write(b"fake video content" * 64)  # 1KB of fake data
    
    try:
        with open(test_video_path, "rb") as video_file:
            files = {"file": ("test_video.mp4", video_file, "video/mp4")}
            response = requests.post(f"{BASE_URL}/videos/upload/", files=files)
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload successful!")
            print(f"   URL: {result.get('url')}")
            print(f"   Filename: {result.get('filename')}")
            print(f"   Size: {result.get('size')} bytes")
            return result.get('url')
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None
    finally:
        # Clean up test file
        if os.path.exists(test_video_path):
            os.remove(test_video_path)

def test_list_videos():
    """Test listing all videos"""
    print("\nTesting list videos...")
    
    try:
        response = requests.get(f"{BASE_URL}/videos/")
        
        if response.status_code == 200:
            result = response.json()
            videos = result.get('videos', [])
            print(f"✅ Found {len(videos)} videos")
            for video in videos:
                print(f"   - {video.get('name')} ({video.get('size')} bytes)")
            return videos
        else:
            print(f"❌ List failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ List error: {e}")
        return []

def test_get_video(blob_name):
    """Test getting a specific video"""
    print(f"\nTesting get video: {blob_name}")
    
    try:
        response = requests.get(f"{BASE_URL}/videos/{blob_name}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Get video successful!")
            print(f"   URL: {result.get('url')}")
            return result.get('url')
        else:
            print(f"❌ Get video failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Get video error: {e}")
        return None

def test_stream_video(blob_name):
    """Test streaming a video"""
    print(f"\nTesting stream video: {blob_name}")
    
    try:
        response = requests.get(f"{BASE_URL}/videos/{blob_name}/stream")
        
        if response.status_code == 200:
            print(f"✅ Stream successful!")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            print(f"   Content-Length: {response.headers.get('content-length')}")
            return True
        else:
            print(f"❌ Stream failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Stream error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting API tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("=" * 50)
    
    # Test upload
    upload_url = test_upload_video()
    
    # Test list videos
    videos = test_list_videos()
    
    # Test get video if we have videos
    if videos:
        first_video = videos[0]
        blob_name = first_video.get('name')
        if blob_name:
            test_get_video(blob_name)
            test_stream_video(blob_name)
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!") 