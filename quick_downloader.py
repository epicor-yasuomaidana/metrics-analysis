import os
from collections import defaultdict

from cache_manager.file_manager import get_csv_files_from_download, get_generated_file, move_generated_file, skip_search
from chrome_utils import GrafanaUrlInputs, ChromeDriver, ChromeOptions

default_titles = [
    "Total Requests per Scenario", "Iterations per Scenario",
    "TTFB per Scenario", "Request Duration per Scenario p99",
    "Avg Iteration Duration p99"]

tables_titles = ["Iterations per Scenario", "Request Duration per Scenario p99", "Avg Iteration Duration p99",
                 "TTFB per Scenario", "Total Requests per Scenario"]

chrome_profile_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data",
                                   "Default")
default_options = ChromeOptions(chrome_profile_path, "Default")

class QuickDownloader:
    def __init__(self, grafana_urls: list[GrafanaUrlInputs], options: ChromeOptions = default_options,
                 dashboards: tuple[str, ...] = tuple(default_titles), tables=tuple(tables_titles),
                 download_path: str = None, group_duration_version: str = "cevpr06yrc0e8a/group-duration"):
        self.grafana_urls = grafana_urls
        self.driver = ChromeDriver(grafana_urls[0], options=options)
        self.dashboards = dashboards
        self.download_path = download_path
        self.tables = tables
        self.group_duration_version = group_duration_version
        self.data = defaultdict(dict)

    def _process_dashboard_title(self, title, instance, starting_date, test_id, forced, section=None):
        original_files = get_csv_files_from_download(self.download_path)
        if test_id:
            destination_path = f"./quick/{instance}_{starting_date}t_id{test_id}_{title}.csv"
        else:
            destination_path = f"./quick/{instance}_{starting_date}{title}.csv"

        if skip_search(destination_path, forced):
            print(f"Skipping {title} as it already exists in {destination_path}")
            return destination_path
        print(f"\033[94mHover {{{title}}}\033[0m")
        self.driver.click_menu_and_inspect_data(title, section)
        input(f"Enter to continue after saving {title}...")
        self.driver.press_key('\u001b')
        generated_file = get_generated_file(original_files, self.download_path)
        move_generated_file(generated_file, destination_path)
        return destination_path

    def download_dashboards(self, test_id: str = None, forced: bool = False, section: str = "General Summary"):
        print("\033[93mDownloading dashboards...\033[0m")

        for grafana_url in self.grafana_urls:
            self.driver.go_to_dashboard(grafana_url.build_url())
            instance = grafana_url.names_space
            starting_date = grafana_url.str_from_ts()

            dashboards = {}
            for title in self.dashboards:
                dashboards[title] = self._process_dashboard_title(title, instance, starting_date, test_id, forced,
                                                                  section)
            grafana_url.version = self.group_duration_version
            self.driver.go_to_dashboard(grafana_url.build_url())
            dashboards["Group Duration"] = self._process_dashboard_title("Group Duration", instance, starting_date,
                                                                         test_id, forced)

            stored_data = self.data.get(f"{grafana_url.names_space}_{grafana_url.identifier}", {})
            stored_data.update({"dashboards": dashboards})
            self.data[f"{grafana_url.names_space}_{grafana_url.identifier}"] = stored_data

    def download_tables(self, test_id: str = None, forced: bool = False):
        print("\033[93mDownloading tables...\033[0m")
        for grafana_url in self.grafana_urls:
            tables = {}
            self.driver.go_to_dashboard(grafana_url.build_url())
            instance = grafana_url.names_space
            starting_date = grafana_url.str_from_ts()
            input(f"Enter to continue ...")
            for title in self.tables:
                if test_id:
                    destination_path = f"./quick/{instance}_{starting_date}t_id{test_id}_{title}_table.csv"
                else:
                    destination_path = f"./quick/{instance}_{starting_date}{title}_table.csv"

                print("Getting table data for:", title)

                if skip_search(destination_path, forced):
                    print(f"Skipping {title} as it already exists in {destination_path}")
                    tables[title] = destination_path
                    continue

                print(f"\033[94mSaving {{{title}}} table\033[0m")
                table_data = self.driver.copy_table(title)
                table_data.to_csv(destination_path, index=False, encoding="utf-8")
                tables[title] = destination_path
            stored_data = self.data.get(f"{grafana_url.names_space}_{grafana_url.identifier}", {})
            stored_data.update({"tables": tables})
            self.data[f"{grafana_url.names_space}_{grafana_url.identifier}"] = stored_data

    def download(self):
        try:
            self.download_tables()
            self.download_dashboards()
        finally:
            self.driver.close()
        return self.data


if __name__ == "__main__":
    from_ts = "2025-08-22 12:50:00"  # Example timestamp
    to_ts = "2025-08-22 14:20:00"  # Example timestamp
    var_scenario = "ARInvoiceTracker"
    resource_groups = "rgQAToolsSaaSAKSResources-EastUS"
    names_space = "perfwamd2"
    grafana_inputs = GrafanaUrlInputs(from_ts, to_ts, names_space, "testing", var_scenario, resource_groups)

    options_ = ChromeOptions(r"C:\Users\yasuo.maidana\AppData\Local\Google\Chrome\User Data\Default",
                             "Default")

    downloader = QuickDownloader([grafana_inputs], options_)
    downloader.download()
    print("Finished")
