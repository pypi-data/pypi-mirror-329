import json
import pkgutil
import requests
from QAnglesKit.auth import AuthManager

class qanglescuda:
    def __init__(self):
        """Load API URLs from config.json and initialize authentication."""
        config_data = pkgutil.get_data("QAnglesKit", "config.json")
        if config_data is None:
            raise FileNotFoundError("config.json not found in package.")

        config = json.loads(config_data.decode("utf-8"))
        self.cudaq_url = config["cudaq_url"]
        self.cudaq_algo_url = config["cudaq_algo_url"]
        self.cudaq_algo_exec_url = config["cudaq_algo_exec_url"]

    def get_cudaq_details(self, domain):
        """Fetch CUDA-Q details for a given Domain."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.post(self.cudaq_url, json={"Domain": domain})
            return response.json().get("Details") if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error fetching CUDA-Q details: {e}")
            return None

    def get_cudaq_algo_details(self, domain, customer, algo_id):
        """Fetch CUDA-Q algorithm details for Domain, Customer, and AlgoID."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.post(self.cudaq_algo_url, json={"Domain": domain, "Customer": customer, "AlgoID": algo_id})
            return response.json().get("Details") if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error fetching CUDA-Q algorithm details: {e}")
            return None

    def get_cudaq_algo_execution_details(self, domain, customer, algo_id, run_id):
        """Fetch CUDA-Q algorithm execution details."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.post(self.cudaq_algo_exec_url, json={"Domain": domain, "Customer": customer, "AlgoID": algo_id, "RunID": run_id})
            return response.json().get("Details") if response.status_code == 200 else None
        except requests.RequestException as e:
            print(f"Error fetching CUDA-Q execution details: {e}")
            return None
