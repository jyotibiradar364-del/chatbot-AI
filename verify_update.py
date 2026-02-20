import requests
import time

def verify_routes():
    base_url = 'http://127.0.0.1:5000'
    
    # Test Dashboard
    try:
        resp = requests.get(base_url + '/')
        if resp.status_code == 200 and 'BroKod' in resp.text:
            print("[PASS] Dashboard loaded successfully.")
        else:
            print(f"[FAIL] Dashboard check failed. Status: {resp.status_code}")
    except Exception as e:
        print(f"[FAIL] Dashboard connection error: {e}")

    # Test Chat Page
    try:
        resp = requests.get(base_url + '/chat')
        if resp.status_code == 200 and 'Welcome' in resp.text:
            print("[PASS] Chat page loaded successfully.")
        else:
            print(f"[FAIL] Chat page check failed. Status: {resp.status_code}")
    except Exception as e:
        print(f"[FAIL] Chat page connection error: {e}")

    # Test Chat API
    try:
        data = {'message': 'Hello'}
        resp = requests.post(base_url + '/api/chat', json=data)
        if resp.status_code == 200:
            print("[PASS] Chat API works.")
        else:
            print(f"[FAIL] Chat API failed. Status: {resp.status_code}")
    except Exception as e:
        print(f"[FAIL] Chat API connection error: {e}")

if __name__ == "__main__":
    time.sleep(2) # Ensure server is up
    verify_routes()
