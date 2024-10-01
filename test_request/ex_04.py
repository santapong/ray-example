import requests

# print(requests.get("http://localhost:8000/").json())
# 3: Query the application and print the result.
print(requests.post("http://localhost:8000/model_4", json={"val": 100.0}).json())
# {"result": 101.5}