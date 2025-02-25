from QAnglesKit.base_api import BaseAPIHandler

class qanglesdashboard(BaseAPIHandler):
    def get_dashboard(self, domain_id, customer):
        """Fetch dashboard details."""
        return self.make_request("dashboard_url", {"DomainID": domain_id, "Customer": customer})
