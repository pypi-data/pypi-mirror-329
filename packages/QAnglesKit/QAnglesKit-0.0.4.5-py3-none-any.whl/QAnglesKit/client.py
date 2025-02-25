import requests
import getpass
import json
import pkgutil

class QuantumJobDetails:
    def __init__(self):
        """
        Load API URLs dynamically from config.json included in the package.
        """
        config_data = pkgutil.get_data("QAnglesKit", "config.json")
        config = json.loads(config_data.decode("utf-8"))

        self.login_url = config["LOGIN_URL"]
        self.fetch_url = config["FETCH_URL"]
        self.store_url = config["STORE_URL"]
        self.get_all_url = config["GET_ALL_URL"]

        self.session = requests.Session()
        self.authenticated = False

    def login(self):
        """
        Authenticate the user interactively via the console.
        :return: True if login is successful, False otherwise.
        """
        username = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")

        customer_id = username.split('@')[1].split('.')[0] if '@' in username else ""

        try:
            response = self.session.post(self.login_url, json={
                "Email": username,
                "password": password,
                "customerID": customer_id
            })
            if response.status_code == 200 and response.json().get("Status") == "Success":
                print("Login successful.")
                self.authenticated = True
                return True
            else:
                print(f"Login failed: {response.status_code} - {response.text}")
                self.authenticated = False
                return False
        except requests.RequestException as e:
            print(f"Error during login: {e}")
            self.authenticated = False
            return False

    def check_authentication(self):
        """
        Check if the user is authenticated.
        :return: None. Raises an exception if not authenticated.
        """
        if not self.authenticated:
            raise Exception("Not authenticated. Please login first.")

    def fetch_job_details(self, job_id):
        """
        Fetch details of a quantum job by its ID.
        :param job_id: ID of the quantum job to retrieve.
        :return: JSON response with job details.
        """
        self.check_authentication()
        try:
            response = self.session.post(self.fetch_url, json={"job_id": job_id})
            if response.status_code == 200:
                return response.json().get("Details")
            else:
                print(f"Failed to fetch job details: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error while fetching job details: {e}")
            return None

    def store_job_details(self, job_data):
        """
        Store new quantum job details in the database.
        :param job_data: Dictionary containing job details.
        :return: JSON response with the status of the operation.
        """
        self.check_authentication()
        try:
            response = self.session.post(self.store_url, json=job_data)
            if response.status_code in [200, 201]:
                print("Job saved successfully.")
                return response.json().get("Details")
            else:
                print(f"Failed to save job: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error while saving job: {e}")
            return None

    def get_all_jobs(self):
        """
        Get all job IDs and titles.
        :return: JSON response with job IDs and titles.
        """
        self.check_authentication()
        try:
            response = self.session.get(self.get_all_url)
            if response.status_code == 200:
                return response.json().get("Details")
            else:
                print(f"Failed to fetch all jobs: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error while fetching all jobs: {e}")
            return None
