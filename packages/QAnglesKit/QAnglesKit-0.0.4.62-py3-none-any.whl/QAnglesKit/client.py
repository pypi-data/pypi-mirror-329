from QAnglesKit.base_api import BaseAPIHandler

class QuantumJobDetails(BaseAPIHandler):
    def fetch_job_details(self, job_id):
        """Fetch details of a quantum job by its ID."""
        return self.make_request("fetch_jobdetails_url", {"job_id": job_id})

    def store_job_details(self, job_data):
        """Store new quantum job details."""
        return self.make_request("store_jobdetails_url", job_data)

    def get_all_jobs(self):
        """Retrieve all stored quantum jobs."""
        return self.make_request("get_all_jobdetails_url")
