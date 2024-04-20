import re
import time
import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 100)

try:
    driver.get("https://www.linkedin.com/login")

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys("EMAIL")
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys("PASSWORD")
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[3]/button"))).click()

    page_start = 0

    while True:
        driver.get(f"https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer&start={page_start}")
        time.sleep(3)
        search_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
        jobs = search_list.find_elements(By.XPATH, "./*[4]/*")
        initial_window_handle = driver.current_window_handle
        for job in jobs:
            driver.execute_script("arguments[0].scrollIntoView(true)", job)
            time.sleep(0.1)

            try:
                job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                continue

            driver.switch_to.new_window("tab")
            driver.get(job_link)

            for window_handle in driver.window_handles:
                if window_handle != initial_window_handle:
                    link_window_handle = window_handle
                    break

            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "div.jobs-apply-button--top-card button.jobs-apply-button"))).click()
            time.sleep(3)

            if len(driver.window_handles) == 3:
                for window_handle in driver.window_handles:
                    if window_handle != initial_window_handle and window_handle != link_window_handle:
                        foreign_window_handle = window_handle
                        break

                driver.switch_to.window(foreign_window_handle)

                for link_element in driver.find_elements(By.CSS_SELECTOR, "*[href]"):
                    link = link_element.get_attribute("href")
                    try:
                        url = urllib.parse.urlparse(link)

                        if re.match(r".*myworkdayjobs\.com", url.hostname):
                            print(url.hostname)
                    except:
                        pass

                driver.close()
                driver.switch_to.window(link_window_handle)
            else:
                pass

            driver.close()

            page_start += 25
            for window_handle in driver.window_handles[:]:
                if window_handle != initial_window_handle:
                    driver.switch_to.window(window_handle)
                    driver.close()
            time.sleep(2)
finally:
    driver.quit()
