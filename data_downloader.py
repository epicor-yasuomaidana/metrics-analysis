from cache_manager.database import init_tables
from chrome_utils import GrafanaUrlInputs, ChromeOptions, ChromeDriver
from cache_manager.file_manager import get_csv_files_from_download


# def click_menu_and_get_new_csv(driver, title:str):
#     starting_csv = get_csv_files_from_download()
#     menu_xpath = f'//h2[@title="{title}"]/ancestor::div[contains(@class,"panel-header")]//button[@title="Menu" and contains(@aria-label,"{title}")]'
#     wait = WebDriverWait(driver, 60)
#     menu_button = wait.until(ec.element_to_be_clickable((By.XPATH, menu_xpath)))
#     menu_button.click()
#
#     driver.switch_to.active_element.send_keys('i')
#     expand_xpath = '//button[@aria-label="Expand query row"]'
#     try:
#         expand_button = wait.until(ec.element_to_be_clickable((By.XPATH, expand_xpath)))
#         expand_button.click()
#     except TimeoutException:
#         print("\t\033[91mExpand button not found, trying to locate it again.\033[0m")
#     except Exception as e:
#         print(e)
#
#     input("Type Enter to continue...")
#     downloaded_csv = get_csv_files_from_download() - starting_csv
#     return downloaded_csv

# def open_chrome_session(url, user_data_dir, profile_directory="Default"):
#     chrome_options = Options()
#     chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
#     chrome_options.add_argument(f"--profile-directory={profile_directory}")
#     chrome_options.add_argument("--remote-debugging-port=9222")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.get(url)
#     if "login" in driver.current_url:
#         print("Redirected to login page.")
#         driver.get(url)
#     navigate_and_download(driver)



# def navigate_and_download(driver):
#
#     downloaded_csv = click_menu_and_get_new_csv(driver,"Total Requests per Scenarios")
#     print(downloaded_csv)



if __name__ == "__main__":
    # Example usage
    from_ts = "now-30m"  # Example timestamp
    to_ts = "now"    # Example timestamp
    var_scenario = "ARInvoiceTracker"
    resource_groups = "rgQAToolsSaaSAKSResources-EastUS"
    names_space = "perfwamd2"

    init_tables()
    grafana_inputs = GrafanaUrlInputs(from_ts, to_ts, var_scenario, resource_groups, names_space)
    options = ChromeOptions(r"C:\Users\yasuo.maidana\AppData\Local\Google\Chrome\User Data\Default",
                            "Default")

    driver = ChromeDriver(grafana_inputs, options)
    driver.click_menu_and_inspect_data("Total Requests per Scenario")
    input("Press Enter to continue...")
    print(get_csv_files_from_download())

    print("Finished")