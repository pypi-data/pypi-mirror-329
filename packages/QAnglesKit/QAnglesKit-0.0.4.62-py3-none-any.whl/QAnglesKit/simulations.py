from QAnglesKit.base_api import BaseAPIHandler

class qanglessimulation(BaseAPIHandler):
    def get_simulation_details_system(self, domain, simulation, customer):
        """Fetch system-based simulation details."""
        return self.make_request("simulation_system_url", {"Domain": domain, "Simulation": simulation, "Customer": customer})

    def get_simulation_details_custom(self, domain, simulation, customer):
        """Fetch custom simulation details."""
        return self.make_request("simulation_custom_url", {"Domain": domain, "Simulation": simulation, "Customer": customer})
