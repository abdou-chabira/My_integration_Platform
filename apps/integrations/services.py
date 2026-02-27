import random
import time

class HubspotClient:
    def __init__(self, access_token):
        self.access_token = access_token

    def create_contact(self, data):
        time.sleep(1)
        if random.random() < 0.2:
            raise Exception("HubSpot API failure")
        return {"id": random.randint(1000, 9999), "email": data.get("email")}