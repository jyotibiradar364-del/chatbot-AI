import requests
import time
import sys

# Windows console cp1252 error workaround
sys.stdout.reconfigure(encoding='utf-8')

def test_chat():
    url = 'http://127.0.0.1:5000/api/chat'
    data = {'message': 'Hello, are you working?'}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Success! Response:", response.json())
        else:
            print(f"Failed with status {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        print("Connection failed. Server might not be up yet.")

if __name__ == "__main__":
    # Wait a bit for server to start if we run this immediately
    time.sleep(2)
    test_chat()
