from locust import HttpUser, task, between

class FastApiTestUser(HttpUser):
    waite_time = between(1, 5)

    @task
    def test_happy_endpoint(self):
        response = self.client.get("")
        if response.status_code == 200:
            print("Success")
        else:
            print(f"Request failed with status code {response.status_code}")