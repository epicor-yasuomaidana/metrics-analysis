from collections import namedtuple
from dataclasses import dataclass

from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

ChromeOptions = namedtuple("ChromeOptions", ["user_data_dir", "profile_directory"])

FromTo = namedtuple("FromTo", ["from_ts", "to_ts"])


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
    aksCluster: str = "aksCluster-EastUS"

    def build_url(self):
        """
        Constructs a Grafana dashboard URL with specified parameters.

        Returns:
            str: The complete URL with parameters.
        """
        base_url = self.base_url + self.version + "?orgId=" + str(self.org_id)
        params = (
            f"&var-Workspace="
            f"&var-AKS={self.aksCluster}"
            # f"&var-ds=beh175ytk7i80c"
            f"&var-sub=KineticQATools"
            f"&var-rg=rgProdSaaSSqlResources-EastUS"
            f"&from={self.from_ts}"
            f"&to={self.to_ts}"
            f"&var-scenario={self.var_scenario}"
            f"&var-ResourceGroups={self.resource_groups}"
            f"&var-Namespace={self.names_space}"
        )
        return base_url + params

    def update_grafana_dashboard(self, from_to: FromTo = None, name_space: str = None, resource_groups: str = None,
                                 var_scenario: str = None):
        if from_to:
            self.from_ts = from_to.from_ts
            self.to_ts = from_to.to_ts
        if name_space:
            self.names_space = name_space
        if resource_groups:
            self.resource_groups = resource_groups
        if var_scenario:
            self.var_scenario = var_scenario


class ChromeDriver:
    def __init__(self, grafana_dashboard: GrafanaUrlInputs, options: ChromeOptions = None):
        if options:
            chrome_options = Options()
            chrome_options.add_argument(f"--user-data-dir={options.user_data_dir}")
            chrome_options.add_argument(f"--profile-directory={options.profile_directory}")
            chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome()
        self.go_to_dashboard(grafana_dashboard.build_url())

    def go_to_dashboard(self, url: str):
        self.driver.get(url)
        if "login" in self.driver.current_url:
            print("\033[91mRedirected to login page.\033[0m")
            input("Press enter to continue...")
            self.driver.get(url)

    def click_menu_and_get_new_csv(self, title: str):
        driver = self.driver

        menu_xpath = f'//h2[@title="{title}"]/ancestor::div[contains(@class,"panel-header")]//button[@title="Menu" and contains(@aria-label,"{title}")]'
        wait = WebDriverWait(driver, 60)
        menu_button = wait.until(ec.element_to_be_clickable((By.XPATH, menu_xpath)))
        menu_button.click()

        driver.switch_to.active_element.send_keys('i')
        expand_xpath = '//button[@aria-label="Expand query row"]'
        try:
            expand_button = wait.until(ec.element_to_be_clickable((By.XPATH, expand_xpath)))
            expand_button.click()
        except (TimeoutException, ElementClickInterceptedException):
            print("\t\033[91mExpand button not found, trying to locate it again.\033[0m")
        except Exception as e:
            print(type(e))
            print(e)
