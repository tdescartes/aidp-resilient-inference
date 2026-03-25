# AIDP Resilient Inference

This project demonstrates a resilient inference pattern using a Circuit Breaker Gateway and a FastAPI Inference Service.

## Structure

```
aidp-resilient-inference/
├── .github/workflows/   # CI/CD (GitHub Actions)
├── data/                # Sample log data for training
├── models/              # Where we store aidp-anomaly-v1.joblib
├── notebooks/           # The Colab notebook (exported as .ipynb)
├── src/
│   ├── gateway.py       # The Circuit Breaker & Proxy code
│   └── inference.py     # The FastAPI ML model code
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run Inference Service (Terminal 1):
   ```bash
   uvicorn src.inference:app --port 8000 --reload
   ```

3. Run Gateway Service (Terminal 2):
   ```bash
   uvicorn src.gateway:app --port 8001 --reload
   ```
