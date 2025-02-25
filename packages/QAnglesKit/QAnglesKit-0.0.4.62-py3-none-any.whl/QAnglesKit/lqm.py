from QAnglesKit.base_api import BaseAPIHandler

class qangleslqm(BaseAPIHandler):
    def get_lqm_details(self, domain, customer):
        """Fetch LQM details."""
        return self.make_request("lqm_details_url", {"Domain": domain, "Customer": customer})

    def get_lqm_all_execution_details(self, domain, customer):
        """Fetch all execution details for LQM."""
        return self.make_request("lqm_all_executions_url", {"Domain": domain, "Customer": customer})

    def get_lqm_execution_details(self, domain, customer, exe_id):
        """Fetch specific execution details for LQM."""
        return self.make_request("lqm_execution_url", {"Domain": domain, "Customer": customer, "ExeID": exe_id})
