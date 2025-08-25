from chrome_utils import GrafanaUrlInputs
from quick_downloader import QuickDownloader

if __name__ == "__main__":
    vus = 494

    from_ts = "2025-08-22 12:50:00"  # Example timestamp
    to_ts = "2025-08-22 14:20:00"  # Example timestamp
    var_scenario = "ARInvoiceTracker"
    resource_groups = "rgQAToolsSaaSAKSResources-EastUS"
    names_space = "perflamd1"
    l1 = GrafanaUrlInputs(from_ts, to_ts, names_space, "l1", vus, var_scenario, resource_groups)

    from_ts = "2025-08-21 18:00:00"  # Example timestamp
    to_ts = "2025-08-21 19:30:00"  # Example timestamp
    var_scenario = "ARInvoiceTracker"
    resource_groups = "rgQAToolsSaaSAKSResources-EastUS"
    names_space = "perfwamd2"
    w2 = GrafanaUrlInputs(from_ts, to_ts, names_space, "l2", vus, var_scenario, resource_groups)

    downloader = QuickDownloader([l1, w2])
    data = downloader.download()
