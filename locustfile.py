from locust import HttpUser, task, between

class DjangoLoadUser(HttpUser):
    wait_time = between(1, 3)  # Temps entre les requêtes

    @task
    def load_homepage(self):
        self.client.get("/")  # Teste la page d'accueil

    @task(3)  # 3x plus fréquent que les autres tâches
    def load_api(self):
        self.client.get("/api/data/")  # Teste une API

    @task
    def post_data(self):
        self.client.post("/submit/", {"data": "test"})  # Teste un formulaire