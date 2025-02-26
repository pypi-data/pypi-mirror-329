import json
import pkgutil
import requests
from QAnglesKit.auth import AuthManager

class qanglesproject:
    def __init__(self):
        """Load API URLs from config.json and initialize authentication."""
        config_data = pkgutil.get_data("QAnglesKit", "config.json")
        if config_data is None:
            raise FileNotFoundError("config.json not found in package.")

        config = json.loads(config_data.decode("utf-8"))
        self.project_url = config["project_url"]

    def get_project_details(self, domain, system_or_custom, customer):
        """Fetch project details based on Domain, System/Custom, and Customer."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.post(self.project_url, json={"Domain": domain, "System": system_or_custom, "Customer": customer})
            return response.json().get("Details") if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error fetching project details: {e}")
            return None
