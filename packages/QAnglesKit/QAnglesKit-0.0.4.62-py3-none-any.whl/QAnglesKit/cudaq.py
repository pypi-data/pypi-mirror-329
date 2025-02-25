from QAnglesKit.base_api import BaseAPIHandler

class qanglescuda(BaseAPIHandler):
    def get_cudaq_details(self, domain):
        """Fetch CUDAQ details for a given domain."""
        return self.make_request("cudaq_details_url", {"Domain": domain})

    def get_cudaq_algo_details(self, domain, customer, algo_id):
        """Fetch algorithm details for a specific domain, customer, and algorithm ID."""
        return self.make_request("cudaq_algo_details_url", {
            "Domain": domain,
            "Customer": customer,
            "AlgoID": algo_id
        })

    def get_cudaq_algo_execution_details(self, domain, customer, algo_id, run_id):
        """Fetch execution details for a specific algorithm run."""
        return self.make_request("cudaq_algo_execution_url", {
            "Domain": domain,
            "Customer": customer,
            "AlgoID": algo_id,
            "runID": run_id
        })
