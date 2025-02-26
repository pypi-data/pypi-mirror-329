import json
import pkgutil
import requests
from QAnglesKit.auth import AuthManager

class qanglessimulation:
    def __init__(self):
        """Load API URLs from config.json and initialize authentication."""
        config_data = pkgutil.get_data("QAnglesKit", "config.json")
        if config_data is None:
            raise FileNotFoundError("config.json not found in package.")

        config = json.loads(config_data.decode("utf-8"))
        self.simulation_url = config["simulation_custom_url"]

        # ✅ Ensure authentication is initialized
        if not AuthManager._login_url:
            AuthManager.initialize(config["login_url"])

    def get_simulation_details(self, QAcustomerID, ProjectID, DomainID):
        """Fetch simulation details based on QAcustomerID, ProjectID, and DomainID."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            payload = {
                "QAcustomerID": QAcustomerID,
                "ProjectID": ProjectID,
                "DomainID": DomainID,
                "start": 0,
                "end": 10
            }
            response = session.post(self.simulation_url, json=payload)
            
            if response.status_code == 200:
                return response.json()
            
            print(f"Failed to fetch simulation details: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching simulation details: {e}")
        return None

