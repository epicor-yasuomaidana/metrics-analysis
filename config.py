from collections import namedtuple
from dataclasses import dataclass

ChromeOptions = namedtuple("ChromeOptions", ["user_data_dir","profile_directory"])

@dataclass
class GrafanaUrlInputs:
    from_ts: int
    to_ts: int
    var_scenario: str
    resource_groups: str
    names_space: str
    base_url: str = "http://mslab-2024:3000/d/"
    version: str = "eevf3vhn0308wd/k6-execution-monitoring-with-scenario-filters"
    org_id: int = 1

    def build_url(self):
        """
        Constructs a Grafana dashboard URL with specified parameters.

        Returns:
            str: The complete URL with parameters.
        """
        base_url = self.base_url + self.version + "?orgId=" + str(self.org_id)
        params = (
            f"&var-Workspace="
            f"&var-AKS=aksCluster-EastUS"
            f"&var-ds=beh175ytk7i80c"
            f"&var-sub=KineticQATools"
            f"&var-rg=rgProdSaaSSqlResources-EastUS"
            f"&from={self.from_ts}"
            f"&to={self.to_ts}"
            f"&var-scenario={self.var_scenario}"
            f"&var-ResourceGroups={self.resource_groups}"
            f"&var-Namespace={self.names_space}"
        )
        return base_url + params
