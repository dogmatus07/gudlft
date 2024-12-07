from locust import HttpUser, task, between
import time

class websiteUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(1, 5)
    
    @task
    def view_index(self):
        """
        Access the index page in less than 5s
        """
        start_time = time.time()
        response = self.client.get("/")
        total_time = time.time() - start_time
        assert total_time < 5, f"Time taken too long: {total_time} seconds"
        
    @task
    def view_summary(self):
        """
        Access the summary page in less than 5s
        """
        start_time = time.time()
        response = self.client.post("/showSummary", data={"email": "john@simplylift.co"})
        total_time = time.time() - start_time
        assert total_time < 5, f"Time taken too long: {total_time} seconds"
    
    @task
    def book_places(self):
        """
        Test booking places
        Update (purchasePlaces) to (book) < 2s
        View the booking page
        """
        self.client.get("/book/Fall Classic/Simply Lift")
        start_time = time.time()
        response = self.client.post("/purchasePlaces", data={
            "competition": "Fall Classic",
            "club": "Simply Lift",
            "places": 2
        })

        total_time = time.time() - start_time
        assert total_time < 2, f"Time taken too long: {total_time} seconds"