import requests
import json

print(requests.get("http://localhost:8000/model_1").json())