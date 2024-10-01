import requests

# 3: Query the application and print the result.
print(requests.get("http://localhost:8000/model_6").json())
# {'result': 'Hello world!'}