import time
import requests
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

# Simple Circuit Breaker Implementation (or use 'pybreaker' library)
class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=10):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED (working), OPEN (blocking), HALF-OPEN (testing)

    def call(self, func, *args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF-OPEN"
            else:
                raise Exception("Circuit is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "HALF-OPEN":
                self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise e

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def reset(self):
        self.failure_count = 0
        self.state = "CLOSED"

app = FastAPI(title="AIDP Gateway")
cb = CircuitBreaker()

INFERENCE_SERVICE_URL = "http://localhost:8000/predict"

class InferenceRequest(BaseModel):
    data: dict

def call_inference_service(payload):
    response = requests.post(INFERENCE_SERVICE_URL, json=payload)
    response.raise_for_status()
    return response.json()

@app.post("/gateway/predict")
async def proxy_predict(request: InferenceRequest):
    try:
        # Wrap the call in the circuit breaker
        result = cb.call(call_inference_service, request.data)
        return result
    except Exception as e:
        if str(e) == "Circuit is OPEN":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail="Service temporarily unavailable (Circuit Broken)"
            )
        raise HTTPException(status_code=500, detail=str(e))
