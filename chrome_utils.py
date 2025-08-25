from collections import namedtuple
from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.common import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

ChromeOptions = namedtuple("ChromeOptions", ["user_data_dir", "profile_directory"])

FromTo = namedtuple("FromTo", ["from_ts", "to_ts"])


def cast_date(ts: int | str) -> int:
    """
    Converts a timestamp to an integer if it is a string representation of a date.

    Args:
        ts (int|str): The timestamp to convert.

    Returns:
        int: The converted timestamp as an integer.
    """
    if isinstance(ts, str) and "now" not in ts:
        dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp() * 1000)
    elif isinstance(ts, str) and "now" in ts:
        if "m" in ts:
            minutes = int(ts.split("now-")[1].replace("m", ""))
            return int((datetime.now().timestamp() - (minutes * 60)) * 1000)
        elif "h" in ts:
            hours = int(ts.split("now-")[1].replace("h", ""))
            return int((datetime.now().timestamp() - (hours * 3600)) * 1000)
    return ts


@dataclass
class GrafanaUrlInputs:
    from_ts: int | str
    to_ts: int | str
    names_space: str
    identifier: str
    var_scenario: str = None
    resource_groups: str = None
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
                f"&from={cast_date(self.from_ts)}"
                f"&to={cast_date(self.to_ts)}"
                + (f"&var-scenario={self.var_scenario}" if self.var_scenario is not None else "")
                + (f"&var-ResourceGroups={self.resource_groups}" if self.resource_groups is not None else "")
                + (f"&var-Namespace={self.names_space}" if self.names_space is not None else "")
        )
        return base_url + params

    def str_from_ts(self) -> str:
        """
        Returns the 'from' timestamp as a string.

        Returns:
            str: The 'from' timestamp formatted as a string.
        """
        if isinstance(self.from_ts, str):
            return self.from_ts.replace(":", "-").replace(" ", "_") + "-"

        return str(self.from_ts)

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

    def click_and_press(self, xpath: str, key: str):
        driver = self.driver

        wait = WebDriverWait(driver, 60)
        button = wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
        button.click()

        driver.switch_to.active_element.send_keys(key)

    def press_key(self, key: str):
        self.driver.switch_to.active_element.send_keys(key)

    def click_menu_and_press(self, title: str, key: str, section: str = None):
        driver = self.driver

        if section:
            menu_xpath = f'//div[div/button[normalize-space(text())="{section}"]]/following-sibling::div[div/section[.//h2[normalize-space(text())="{title}"]]]'
        else:
            menu_xpath = f'//h2[@title="{title}"]/ancestor::div[contains(@class,"panel-header")]//button[@title="Menu" and contains(@aria-label,"{title}")]'

        wait = WebDriverWait(driver, 60)
        menu_button = wait.until(ec.element_to_be_clickable((By.XPATH, menu_xpath)))
        menu_button.click()

        driver.switch_to.active_element.send_keys(key)

    def copy_table(self, title: str):
        self.click_and_press(rf'//h2[@title="{title}"]', 'v')
        driver = self.driver
        # Locate the panel by its title
        panel_xpath = f'//h2[@title="{title}"]/ancestor::section'
        wait = WebDriverWait(driver, 60)
        wait.until(ec.presence_of_element_located((By.XPATH, panel_xpath)))
        panel = driver.find_element(By.XPATH, panel_xpath)

        table_body_xpath = './/div[@role="row"]'
        rows = panel.find_elements(By.XPATH, table_body_xpath)

        rows_iter = iter(rows)
        header_cells = next(rows_iter).find_elements(By.XPATH, './/div[@role="columnheader"]')
        columns = [cell.text for cell in header_cells]

        table_data = [
            [cell.text for cell in row.find_elements(By.XPATH, './/div[@role="cell"]')]
            for row in rows_iter
        ]

        driver.switch_to.active_element.send_keys('\u001b')  # Press Escape key

        return pd.DataFrame(table_data, columns=columns)

    def click_menu_and_inspect_data(self, title: str, section: str = None):
        driver = self.driver

        wait = WebDriverWait(driver, 60)
        self.click_menu_and_press(title, 'i', section)
        expand_xpath = '//button[@aria-label="Expand query row"]'
        try:
            expand_button = wait.until(ec.element_to_be_clickable((By.XPATH, expand_xpath)))
            expand_button.click()
        except (TimeoutException, ElementClickInterceptedException):
            print("\t\033[91mExpand button not found, trying to locate it again.\033[0m")
        except Exception as e:
            print(type(e))
            print(e)

    def close(self):
        """
        Closes the Chrome driver.
        """
        self.driver.quit()
