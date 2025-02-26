import json
import pkgutil
import requests
from QAnglesKit.auth import AuthManager

class QAnglesDashboard:
    def __init__(self):
        """Load API URLs from config.json and initialize authentication."""
        config_data = pkgutil.get_data("QAnglesKit", "config.json")
        if config_data is None:
            raise FileNotFoundError("config.json not found in package.")

        config = json.loads(config_data.decode("utf-8"))
        self.dashboard_url = config["dashboard_url"]

    def get_dashboard(self, domain_id, customer):
        """Fetch dashboard data based on DomainID and Customer."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.post(self.dashboard_url, json={"DomainID": domain_id, "Customer": customer})
            return response.json().get("Details") if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error fetching dashboard data: {e}")
            return None
