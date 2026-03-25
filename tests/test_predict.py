import requests
import time

BASE = "http://127.0.0.1:8000"

def wait_health(timeout=10):
    for i in range(timeout*2):
        try:
            r = requests.get(f"{BASE}/health", timeout=2)
            if r.status_code == 200:
                print("Health OK:", r.text)
                return True
        except Exception:
            pass
        time.sleep(0.5)
    print("Health check failed")
    return False

tests = [
    ("Normal data", {"CPU_Percent": 10, "Memory_Percent": 20, "Latency_ms": 30}),
    ("Anomalous data", {"CPU_Percent": 95, "Memory_Percent": 90, "Latency_ms": 900}),
    ("Missing field", {"CPU_Percent": 10, "Latency_ms": 30}),
    ("Invalid types", {"CPU_Percent": "high", "Memory_Percent": "low", "Latency_ms": "fast"}),
    ("List payload", [{"CPU_Percent": 10, "Memory_Percent": 20, "Latency_ms": 30}, {"CPU_Percent": 95, "Memory_Percent": 90, "Latency_ms": 900}])
]

def run_tests():
    if not wait_health():
        return

    for name, payload in tests:
        try:
            r = requests.post(f"{BASE}/predict", json=payload, timeout=5)
            print(f"--- {name} ---")
            print("Status:", r.status_code)
            try:
                print("Response JSON:", r.json())
            except Exception:
                print("Response Text:", r.text)
        except Exception as e:
            print(f"--- {name} ERROR ---\n", e)

if __name__ == '__main__':
    run_tests()
