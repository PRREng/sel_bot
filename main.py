from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import argparse

import util


parser = argparse.ArgumentParser(description="Fazer Relatório baseado em mês e ano")
parser.add_argument("--mes", "-m",  help="mês do relatório (e.g., '11'", required=True)
parser.add_argument("--ano", "-a", help="ano do relatório (e.g., '2024'", required=True)

args = parser.parse_args()



download_path = os.path.join(os.path.dirname(__file__), f"{args.mes} {args.ano}")

options = Options()
# download_path = download_path
options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

driver.get("https://gdash.io")

signin_element = driver.find_element(By.CSS_SELECTOR, ".shadepro-btn.btn-type-boxed.elementor-animation-")
# input_element.send_keys("tech with tim" + Keys.ENTER)
email = ""
password = ""
signin_element.click()

wait = WebDriverWait(driver, 5)
email_element = driver.find_element(By.ID, "login")
pass_element = driver.find_element(By.ID, "pw")

email_element.send_keys(email)
time.sleep(3)
pass_element.send_keys(password + Keys.ENTER)

usinas_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".relative.rounded-lg.p-2.bg-none")))
usinas_element.click()

time.sleep(5)

download_list_element = driver.find_element(By.CSS_SELECTOR, ".hidden.h-9.items-center")
download_list_element.click()

time.sleep(5)

export_buttons = driver.find_elements(By.CSS_SELECTOR, 'button[data-test="button-delete-customer"]')

for button in export_buttons:
    button_text = button.text.strip()
    if button_text == "Exportar em .csv":
        button.click()  # here is where it is going to download
        break

time.sleep(5)


clientes = util.get_ProList(download_path)
if clientes is None:
    clientes = []
time.sleep(5)
print(f"Quantidade de clientes Pro: {len(clientes)}")

for client in clientes:
    input_xpath = "/html/body/div[1]/div[3]/div/div/main/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/input"
    search_elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, input_xpath))
    )
    # client = "Carlos Lapa"
    print(f"Current client: {client}")
    search_elem.send_keys(client)
    time.sleep(2)

    # find the right client
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
    )
    time.sleep(2)

    # Iterate through rows to find the specific client
    found = False
    for row in rows:
        # Get the list of <td> elements in the row
        cells = WebDriverWait(driver, 10).until(
            lambda d: row.find_elements(By.TAG_NAME, "td")
        )
        # cells = WebDriverWait(driver, 10).until(
        #     EC.presence_of_all_elements_located((By.TAG_NAME, "td"))
        # )
        # Check if any of the cells contain the client name
        for cell in cells:
            if client in cell.text:
                # If the client name is found, click the row or perform the desired action
                row.click()  # Or cell.click() if clicking the cell is needed
                print(f"Clicked on row with client: {client}")
                found = True
                break
        if found:
            break

    if not found:
        print("Cliente {client} não foi encontrado")
        continue

    # look for the one with same client name
    # found_elem.click()
    time.sleep(2)

    month_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-test="power-plant-month-chart-tab"]'))
    )
    month_elem.click()
    time.sleep(2)

    button_xpath = '//*[@id="gdash-main-scroll"]/div/div/main/div[2]/div/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[1]/button[1]'
    button_element = driver.find_element(By.XPATH, button_xpath)
    button_element.click()
    time.sleep(2)

    customer_elem = driver.find_element(By.CSS_SELECTOR, 'button[data-test="show-customer-actions-button"]')
    customer_elem.click()
    time.sleep(2)

    export_client_elem = driver.find_elements(By.CSS_SELECTOR, 'button[data-test="button-delete-customer"')
    for button in export_client_elem:
        button_text = button.text.strip()
        if button_text == "Exportar em .csv":
            button.click()  # here is where it is going to download
            break
    time.sleep(2)

    report = driver.find_element(By.XPATH, '//*[@id="gdash-main-scroll"]/div/div/nav/div/div[1]/a[4]')
    report.click()
    time.sleep(2)

    original_window = driver.current_window_handle

    try:
        # Wait for the table to load
        table_xpath = "//table/tbody/tr"
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, table_xpath))
        )

        # Find the row containing "Novembro"
        desired_month = util.month[int(args.mes)]
        desired_year = args.ano
        message = f"{desired_month} {desired_year}"
        print(f"Desired message : {message}")
        month_row_xpath = f"//table/tbody/tr[td[contains(text(), '{message}')]]"
        month_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, month_row_xpath))
        )

        # Perform an action on the row (e.g., click)
        print(f"ROW FOUND: {month_row.text}")
        month_row.click()
        print(f"Clicked on the row containing '{desired_month}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    # report_btn = driver.find_elements(By.CSS_SELECTOR, ".cursor-pointer.transition-all")
    # clickable_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable(report_btn[1])
    # )
    # clickable_button.click()
    time.sleep(2)

# switched to new tab
    new_window = [window for window in driver.window_handles if window != original_window][0]
    driver.switch_to.window(new_window)
    time.sleep(2)

    # It is hard to use it
    graph_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
                                        '/html/body/div[1]/div[2]/div/div[2]/div/div/button'))
    )
    graph_elem.click()
    # graph_elem = driver.find_element(By.XPATH, '//*[@id="headlessui-menu-button-:r1:"]/svg[1]/path')
    # graph_elem.click()
    time.sleep(2)

    day_elem = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div/div/div/button[2]')
    day_elem.click()
    time.sleep(2)

    down_elem = driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div/button[1]')
    down_elem.click()
    time.sleep(5)

    driver.close()  # Close the new tab
    driver.switch_to.window(original_window)  # Switch back to the original tab
    time.sleep(2)

# rename file
    util.rename_file(download_path, client, args.mes, args.ano)

    driver.get("https://app.gdash.io/g/plants")
    time.sleep(2)


time.sleep(10)

driver.quit()
