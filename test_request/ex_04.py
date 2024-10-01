import requests

# print(requests.get("http://localhost:8000/").json())
# 3: Query the application and print the result.
print(requests.post("http://localhost:8000/Ingress", json={"val": 100.0}).json())
# {"result": 101.5}