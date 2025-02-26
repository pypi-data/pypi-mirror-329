import json
import pkgutil
import requests
from QAnglesKit.auth import AuthManager

class qanglesdashboard:
    def __init__(self):
        """Load API URLs from config.json and initialize authentication."""
        config_data = pkgutil.get_data("QAnglesKit", "config.json")
        if config_data is None:
            raise FileNotFoundError("config.json not found in package.")

        config = json.loads(config_data.decode("utf-8"))
        self.dashboard_url = config["dashboard_url"]

        # ✅ Ensure authentication is initialized
        if not AuthManager._login_url:
            AuthManager.initialize(config["login_url"])

    def get_dashboard(self, domain_id, customer,userID):
        """Fetch dashboard data based on DomainID and Customer."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.post(self.dashboard_url, json={"QAcustomerID": customer, "DomainID": domain_id,"userID": userID,"Key" : 1})
            if response.status_code == 200:
                return response.json().get("boxesdata2")
            print(f"Failed to fetch dashboard data: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching dashboard data: {e}")
        return None
