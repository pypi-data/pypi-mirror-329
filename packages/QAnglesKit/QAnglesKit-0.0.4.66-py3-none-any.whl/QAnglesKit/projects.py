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
        self.project_url = config["project_system_url"]

        
        if not AuthManager._login_url:
            AuthManager.initialize(config["login_url"])

    def get_project_details(self, QAcustomerID, DomainID, userID,projectType):
        """Fetch project details based on Domain, System/Custom, and Customer."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.post(self.project_url, json={
                "QAcustomerID": QAcustomerID,
                "DomainID": DomainID,
                "start" : 0,
                "end" : 10,
                "userID": userID,
                "projectType": projectType
            })
            if response.status_code == 200:
                return response.json()
            print(f"Failed to fetch project details: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching project details: {e}")
        return None
