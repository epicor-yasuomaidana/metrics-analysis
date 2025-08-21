from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from config import GrafanaUrlInputs, ChromeOptions, build_grafana_url
from file_manager import get_csv_files_from_download


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

def open_chrome_session(url, user_data_dir, profile_directory="Default"):
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

def navigate_and_download(grafana_info: GrafanaUrlInputs, boards:list[str]):
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

    open_chrome_session(url, user_data_dir_i)



    print("Finished")