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

        
        if not AuthManager._login_url:
            AuthManager.initialize(config["login_url"])

    def get_cudaq_details(self):
        """Fetch and format CUDA-Q algorithm details."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            response = session.get(self.cudaq_url)  # No domain in URL
            if response.status_code == 200:
                data = response.json()
                return [
                    {
                        "AlgoName": algo["AlgoName"],
                        "AlgoID": algo["AlgoID"],
                       
                    }
                    for algo in data
                ]
            print(f"Failed to fetch CUDA-Q details: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching CUDA-Q details: {e}")
        return None



    def get_cudaq_algo_details(self, AlgoId):
        """Fetch CUDA-Q algorithm details using AlgoID in the URL."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            url = f"{self.cudaq_algo_url}?AlgoID={AlgoId}"  # Passing AlgoID in the URL
            response = session.get(url)  # GET request without payload
            if response.status_code == 200:
                return response.json()
            print(f"Failed to fetch CUDA-Q algorithm details: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching CUDA-Q algorithm details: {e}")
        return None


    def get_cudaq_algo_execution_details(self, algo_name, hardware_run_id, qa_customer_id, algo_run_id):
        """Fetch CUDA-Q algorithm execution details using GET request with query parameters."""
        AuthManager.check_authentication()
        try:
            session = AuthManager.get_session()
            params = {
                "AlgoName": algo_name,
                "HardwareRunID": hardware_run_id,
                "QAcustomerID": qa_customer_id,
                "AlgoRunID": algo_run_id
            }
            response = session.get(self.cudaq_algo_exec_url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                # Exclude HardwareCircuitDiagram
                if "HardwareCircuitDiagram" in data:
                    del data["HardwareCircuitDiagram"]

                # Print formatted details
                for key, value in data.items():
                    print(f"{key}: {value}")
                
                return data
            print(f"Failed to fetch CUDA-Q execution details: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error fetching CUDA-Q execution details: {e}")
        return None

