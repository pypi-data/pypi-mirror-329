from QAnglesKit.base_api import BaseAPIHandler

class qanglesproject(BaseAPIHandler):
    def get_project_details_system(self, domain, customer):
        """Fetch project details for system-based projects."""
        return self.make_request("project_system_url", {"Domain": domain, "Customer": customer})

    def get_project_details_custom(self, domain, customer):
        """Fetch project details for custom projects."""
        return self.make_request("project_custom_url", {"Domain": domain, "Customer": customer})
