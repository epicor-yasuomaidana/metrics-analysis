from collections import namedtuple

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

def get_csv_files_from_download(download_path=r"C:\Users\yasuo.maidana\Downloads"):
    import os

    # Ensure the download path exists
    if not os.path.exists(download_path):
        raise ValueError(f"The specified download path does not exist: {download_path}")

    # Use glob to find all CSV files in the download directory
    csv_files = [f for f in os.listdir(download_path) if f.lower().endswith('.csv')]

    return set(csv_files)


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

def click_menu_and_get_new_csv(driver, title):
    starting_csv = get_csv_files_from_download()
    menu_xpath = f'//h2[@title="{title}"]/ancestor::div[contains(@class,"panel-header")]//button[@title="Menu" and contains(@aria-label,"{title}")]'
    wait = WebDriverWait(driver, 60)
    menu_button = wait.until(ec.element_to_be_clickable((By.XPATH, menu_xpath)))
    menu_button.click()

    driver.switch_to.active_element.send_keys('i')
    expand_xpath = '//button[@aria-label="Expand query row"]'
    try:
        expand_button = wait.until(ec.element_to_be_clickable((By.XPATH, expand_xpath)))
        expand_button.click()
    except Exception as e:
        print("Error locating the expand button")

    input("Type Enter to continue...")
    downloaded_csv = get_csv_files_from_download() - starting_csv
    print(downloaded_csv)
    return downloaded_csv

def open_existing_chrome_session(url, user_data_dir, profile_directory="Default"):
    chrome_options = Options()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument(f"--profile-directory={profile_directory}")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    if "login" in driver.current_url:
        print("Redirected to login page.")
        driver.get(url)


    starting_csv = get_csv_files_from_download()
    menu_xpath = '//h2[@title="Reqs per Scenario"]/ancestor::div[contains(@class,"panel-header")]//button[@title="Menu" and contains(@aria-label,"Reqs per Scenario")]'
    # Selenium code to click the menu
    wait = WebDriverWait(driver, 60)
    menu_button = wait.until(ec.element_to_be_clickable((By.XPATH, menu_xpath)))
    menu_button.click()

    driver.switch_to.active_element.send_keys('i')
    expand_xpath = '//button[@aria-label="Expand query row"]'
    try:
        expand_button = wait.until(ec.element_to_be_clickable((By.XPATH, expand_xpath)))
        expand_button.click()
    except Exception as e:
        print("Error locating the expand button")


    input("Type Enter to continue...")
    downloaded_csv = get_csv_files_from_download() - starting_csv
    print(downloaded_csv)


    return driver

def navigate_and_download(grafana_info:GrafanaUrlInputs, boards:list[str]):
    url = build_grafana_url(grafana_info)



if __name__ == "__main__":
    # Example usage
    from_ts = 1755728580000  # Example timestamp
    to_ts = 1755733259000    # Example timestamp
    var_scenario = "POEntry10"
    resource_groups = "rgQAToolsSaaSAKSResources-EastUS"
    names_space = "perfwamd2"

    # Example usage:
    user_data_dir_i = r"C:\Users\yasuo.maidana\AppData\Local\Google\Chrome\User Data\Default"

    grafana_inputs = GrafanaUrlInputs(from_ts, to_ts, var_scenario, resource_groups, names_space)
    url = build_grafana_url(grafana_inputs)
    print(ChromeOptions(
        user_data_dir=user_data_dir_i,
        profile_directory="Default"
    ))
    print(url)

    open_existing_chrome_session(url, user_data_dir_i)



    print("Finished")