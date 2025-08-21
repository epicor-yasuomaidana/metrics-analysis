from collections import namedtuple

GrafanaUrlInputs = namedtuple("GrafanaUrlInputs", ["from_ts", "to_ts", "var_scenario", "resource_groups", "names_space"])
ChromeOptions = namedtuple("ChromeOptions", ["user_data_dir","profile_directory"])


def build_grafana_url(grafana_inputs: GrafanaUrlInputs):
    """
    Constructs a Grafana dashboard URL with specified parameters.

    Args:
        grafana_inputs (GrafanaUrlInputs): Named tuple containing all required URL parameters:
                - from_ts (int): The 'from' timestamp.
                - to_ts (int): The 'to' timestamp.
                - var_scenario (str): The scenario filter value.
                - resource_groups (str): The resource groups value.
                - names_space (str): The namespace value.

    Returns:
        str: The complete URL with parameters.
    """
    base_url = (
        "http://mslab-2024:3000/d/eevf3vhn0308wd/k6-execution-monitoring-with-scenario-filters"
        "?orgId=1"
        "&var-Workspace="
        "&var-AKS=aksCluster-EastUS"
        "&var-ds=beh175ytk7i80c"
        "&var-sub=KineticQATools"
        "&var-rg=rgProdSaaSSqlResources-EastUS"
    )
    params = (
        f"&from={grafana_inputs.from_ts}"
        f"&to={grafana_inputs.to_ts}"
        f"&var-scenario={grafana_inputs.var_scenario}"
        f"&var-ResourceGroups={grafana_inputs.resource_groups}",
        f"&var-Namespace={grafana_inputs.names_space}"
    )
    return base_url + "".join(params)
