from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def myapp(self):
        self.client.get("/myapp/")
