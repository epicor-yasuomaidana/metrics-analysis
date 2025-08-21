from cache_manager.file_manager import get_csv_files_from_download, get_generated_file, move_generated_file
from chrome_utils import GrafanaUrlInputs, ChromeDriver, ChromeOptions

default_titles = [
    "Total Requests per Scenario", "TTFB per Scenario",
    "Iteration per Scenario", "Request Duration per Scenario p99",
    "Avg Iteration Duration p99"]


class QuickDownloader:
    def __init__(self, grafana_urls: list[GrafanaUrlInputs], options: ChromeOptions,
                 dashboards: list[str] = tuple(default_titles), download_path: str = None):
        self.grafana_urls = grafana_urls
        self.driver = ChromeDriver(grafana_urls[0], options=options)
        self.dashboards = dashboards
        self.download_path = download_path

    def download(self, test_id: str = None):
        for grafana_url in self.grafana_urls:
            self.grafana_urls = grafana_url
            self.driver.go_to_dashboard(grafana_url.build_url())
            instance = grafana_url.names_space
            starting_date = grafana_url.str_from_ts()
            for title in self.dashboards:
                print(f"\033[94mHover {{{title}}}\033[0m")
                original_files = get_csv_files_from_download(self.download_path)
                self.driver.click_menu_and_inspect_data(title)
                input(f"Enter to continue after saving {title}...")
                generated_file = get_generated_file(original_files, self.download_path)
                destination_path = f"./quick/{instance}_{starting_date}_{test_id}_{title}.csv"
                move_generated_file(generated_file, destination_path)
                input("Press Enter to continue...")



if __name__ == "__main__":
    from_ts = "now-30m"  # Example timestamp
    to_ts = "now"  # Example timestamp
    var_scenario = "ARInvoiceTracker"
    resource_groups = "rgQAToolsSaaSAKSResources-EastUS"
    names_space = "perfwamd2"

    grafana_inputs = GrafanaUrlInputs(from_ts, to_ts, var_scenario, resource_groups, names_space)
    options_ = ChromeOptions(r"C:\Users\yasuo.maidana\AppData\Local\Google\Chrome\User Data\Default",
                            "Default")

    downloader = QuickDownloader([grafana_inputs], options_)
    downloader.download()
    input("Press Enter to finish...")

    print("Finished")
