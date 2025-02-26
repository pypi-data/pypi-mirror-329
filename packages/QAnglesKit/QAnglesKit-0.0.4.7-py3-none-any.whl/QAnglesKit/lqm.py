import json
import pkgutil
import requests
from QAnglesKit.auth import AuthManager

class qangleslqm:
    def __init__(self):
        """Load API URLs from config.json and initialize authentication."""
        config_data = pkgutil.get_data("QAnglesKit", "config.json")
        if config_data is None:
            raise FileNotFoundError("config.json not found in package.")

        config = json.loads(config_data.decode("utf-8"))
        self.lqm_url = config["lqm_details_url"]

        # ✅ Ensure authentication is initialized
        if not AuthManager._login_url:
            AuthManager.initialize(config["login_url"])

    def get_lqm_details(self, domain, customer):
        """Fetch LQM details for a given Domain and Customer using GET request."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.get(f"{self.lqm_url}?DomainID={domain}&QAcustomerID={customer}")  # Using GET with query params
            
            if response.status_code == 200:
                return response.json().get("Details")

            print(f"Failed to fetch LQM details: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching LQM details: {e}")
        return None


    # def get_lqm_all_execution_details(self, domain, customer):
    #     """Fetch all LQM execution details for a given Domain and Customer."""
    #     AuthManager.check_authentication()
    #     try:
    #         session = AuthManager.get_session()
    #         response = session.post(self.lqm_url, json={"Domain": domain, "Customer": customer, "Type": "AllExecutions"})
    #         if response.status_code == 200:
    #             return response.json().get("Details")
    #         print(f"Failed to fetch all LQM execution details: {response.status_code}")
    #     except requests.RequestException as e:
    #         print(f"Error fetching all LQM execution details: {e}")
    #     return None

    # def get_lqm_execution_details(self, domain, customer, exe_id):
    #     """Fetch specific LQM execution details for a given Execution ID."""
    #     AuthManager.check_authentication()
    #     try:
    #         session = AuthManager.get_session()
    #         response = session.post(self.lqm_url, json={"Domain": domain, "Customer": customer, "ExeID": exe_id})
    #         if response.status_code == 200:
    #             return response.json().get("Details")
    #         print(f"Failed to fetch LQM execution details: {response.status_code}")
    #     except requests.RequestException as e:
    #         print(f"Error fetching LQM execution details: {e}")
    #     return None
