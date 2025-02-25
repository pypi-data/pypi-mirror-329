from QAnglesKit.base_api import BaseAPIHandler

class qanglesqcircuit(BaseAPIHandler):
    def get_qcircuit_details(self, domain, customer):
        """Fetch quantum circuit details."""
        return self.make_request("qcircuit_details_url", {"Domain": domain, "Customer": customer})

    def get_qcircuit_code_details(self, domain, customer, circuit_id):
        """Fetch quantum circuit code details."""
        return self.make_request("qcircuit_code_url", {"Domain": domain, "Customer": customer, "Circuitid": circuit_id})

    def get_qcircuit_all_execution_details(self, domain, customer, circuit_id):
        """Fetch all execution details of a quantum circuit."""
        return self.make_request("qcircuit_all_executions_url", {"Domain": domain, "Customer": customer, "Circuitid": circuit_id})

    def get_qcircuit_execution_details(self, domain, customer, circuit_id, run_id):
        """Fetch execution details for a specific quantum circuit run."""
        return self.make_request("qcircuit_execution_url", {"Domain": domain, "Customer": customer, "Circuitid": circuit_id, "RunID": run_id})
