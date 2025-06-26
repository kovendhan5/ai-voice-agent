import requests
import json

def test_server():
    try:
        # Test basic connection
        print("🔍 Testing server connection...")
        response = requests.get("http://localhost:8080/", timeout=5)
        print(f"✅ Server status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
        
        # Test chat endpoint
        print("\n🔍 Testing chat endpoint...")
        chat_data = {
            "message": "Hello, can you hear me?",
            "user_id": "test_user"
        }
        
        chat_response = requests.post(
            "http://localhost:8080/chat", 
            json=chat_data,
            timeout=10
        )
        print(f"✅ Chat status: {chat_response.status_code}")
        print(f"💬 AI Response: {chat_response.json()}")
        
        print("\n🎉 Server is working perfectly!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running on port 8080")
        print("👉 Please start the server first")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_server()
