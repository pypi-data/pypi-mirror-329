import json
import pkgutil
import requests
from QAnglesKit.auth import AuthManager

class qanglesqcircuit:
    def __init__(self):
        """Load API URLs from config.json and initialize authentication."""
        config_data = pkgutil.get_data("QAnglesKit", "config.json")
        if config_data is None:
            raise FileNotFoundError("config.json not found in package.")

        config = json.loads(config_data.decode("utf-8"))
        self.qcircuit_url = config["qcircuit_url"]

        # ✅ Ensure authentication is initialized
        if not AuthManager._login_url:
            AuthManager.initialize(config["login_url"])

    def get_qcircuit_details(self, domain, customer):
        """Fetch quantum circuit details for a given Domain and Customer."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.post(self.qcircuit_url, json={"Domain": domain, "Customer": customer})
            if response.status_code == 200:
                return response.json().get("Details")
            print(f"Failed to fetch quantum circuit details: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching quantum circuit details: {e}")
        return None
