from dataclasses import dataclass

from downloader.chrome_utils import GrafanaUrlInputs

@dataclass
class DashBoardConfig(GrafanaUrlInputs):
    dashboards: tuple[tuple[str, tuple[str,...]],...]
    var_scenario: str = None
    resource_groups: str = None
    base_url: str = "http://mslab-2024:3000/d/"
    version: str = "eevf3vhn0308wd/k6-execution-monitoring-with-scenario-filters"
    org_id: int = 1
    aksCluster: str = "aksCluster-EastUS"
