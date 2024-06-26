import asyncio
import json
import time
import urllib.parse
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import ChatGPTPrompter

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10000)

with open("public/uploads/LinkedInForm.json") as exec_file:
    exec_data = json.load(exec_file)

try:
    driver.get("https://www.linkedin.com/login")

    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(exec_data["email"])
    wait.until(EC.presence_of_element_located((By.ID, "password"))).send_keys(exec_data["password"])
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[3]/button"))).click()

    page_start = 0

    time.sleep(10)

    search_query = urllib.parse.quote_plus(exec_data["searchQuery"])
    location = urllib.parse.quote_plus(exec_data["location"])
    remote = 1
    if exec_data["remote"] == "Remote":
        remote = 2
    elif exec_data["remote"] == "Hybrid":
        remote = 3
    job_type = "I"
    if exec_data["jobType"] == "Full-time":
        job_type = "F"
    elif exec_data["jobType"] == "Part-time":
        job_type = "P"
    elif exec_data["jobType"] == "Contract":
        job_type = "C"
    elif exec_data["jobType"] == "Temporary":
        job_type = "T"
    elif exec_data["jobType"] == "Volunteer":
        job_type = "V"
    elif exec_data["jobType"] == "Other":
        job_type = "O"
    experience_level = 1
    if exec_data["experienceLevel"] == "Entry Level":
        experience_level = 2
    elif exec_data["experienceLevel"] == "Associate":
        experience_level = 3
    elif exec_data["experienceLevel"] == "Mid-Senior level":
        experience_level = 4
    elif exec_data["experienceLevel"] == "Director":
        experience_level = 5
    elif exec_data["experienceLevel"] == "Executive":
        experience_level = 6

    query_begin = f"?keywords={search_query}&location={location}&f_WT={remote}&f_AL=true&f_JT={job_type}&f_E={experience_level}"

    while True:
        driver.get(f"https://www.linkedin.com/jobs/search/{query_begin}&start={page_start}")
        time.sleep(3)
        search_list = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
        jobs = search_list.find_elements(By.XPATH, "./*[4]/*")
        initial_window_handle = driver.current_window_handle
        for job in jobs:
            driver.execute_script("arguments[0].scrollIntoView(true)", job)
            time.sleep(0.1)

            split_by_newline = job.text.split("\n")

            if "Applied" in split_by_newline[-1]:
                job.find_element(By.CSS_SELECTOR, "[aria-label^=\"Dismiss\"]").click()
                continue

            stdout_info = [split_by_newline[0], split_by_newline[1]]

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
                driver.close()
                driver.switch_to.window(link_window_handle)
            else:
                early_leave = False
                try:
                    follow_checkbox = driver.find_element(By.ID, "follow-company-checkbox")
                    if follow_checkbox.get_attribute("checked") == "true":
                        driver.execute_script("arguments[0].click()", follow_checkbox)

                    driver.find_element(By.CSS_SELECTOR, "[aria-label=\"Submit application\"]").click()
                    print(json.dumps(stdout_info))
                    early_leave = True
                except:
                    pass

                if not early_leave:
                    try:
                        while True:
                            for question in driver.find_elements(By.CSS_SELECTOR,
                                                                 ".jobs-easy-apply-form-section__grouping"):
                                try:
                                    question.find_element(By.CSS_SELECTOR, "[class*=\"required\"]")
                                except:
                                    continue

                                try:
                                    fieldset_target = question.find_element(By.CSS_SELECTOR, "fieldset")
                                    try:
                                        question_label = fieldset_target.find_element(By.CSS_SELECTOR, "legend")
                                        answer_labels = fieldset_target.find_elements(By.CSS_SELECTOR, "label")

                                        answer_to_label = {}
                                        for label in answer_labels:
                                            answer_to_label[label.text] = label

                                        opts_prompt = ", ".join(map(lambda opt: f"\"{opt}\"", answer_to_label.keys()))
                                        prompt = f"Answer the following question to the best of your ability from my perspective, based on the information I have given you. If you are unsure of your answer, choose an answer that makes sense for an average person. You have a limited number of choices, and you MUST select one of these choices. The choices are: {opts_prompt}. Use one of these choices exactly. You MUST respond with one of these options. The question is: {question_label.text}"
                                        while True:
                                            response = asyncio.run(ChatGPTPrompter.get_response(prompt))
                                            if response in answer_to_label.keys():
                                                break

                                        chosen_label = answer_to_label[response]
                                        chosen_input = driver.find_element(By.ID, chosen_label.get_attribute("for"))
                                        driver.execute_script("arguments[0].click()", chosen_input)
                                    except:
                                        pass
                                    continue
                                except:
                                    pass

                                question_label = question.find_element(By.CSS_SELECTOR, "label")
                                targeted = driver.find_element(By.ID, question_label.get_attribute("for"))
                                if (targeted.tag_name == "input" and targeted.get_attribute("value") != "") or (
                                        targeted.tag_name == "select" and targeted.get_attribute("value") != "Select an option"):
                                    continue

                                if targeted.tag_name == "input":
                                    prompt = f"Answer the following question to the best of your ability from my perspective, based on the information I have given you. If you are unsure of your answer, write N/A. Speak from my perspective, rather than from yours. The question is: {question_label.text}"

                                    while True:
                                        try:
                                            response = asyncio.run(ChatGPTPrompter.get_response(prompt))
                                            targeted.clear()
                                            time.sleep(0.5)
                                            targeted.send_keys(response)
                                            time.sleep(1)

                                            error_message = question.find_element(By.CSS_SELECTOR,
                                                                                  ".artdeco-inline-feedback__message")
                                            prompt = f"Answer the following question to the best of your ability from my perspective, based on the information I have given you. If you are unsure of your answer, write N/A. Speak from my perspective, rather than from yours. MAKE SURE to follow the following constraint: {error_message.text}. Your response must follow that constraint exactly. The question is: {question_label.text}"
                                        except:
                                            break
                                elif targeted.tag_name == "select":
                                    children = targeted.find_elements(By.XPATH, "./*")
                                    if len(children) > 0:
                                        opts = list(map(lambda e: e.text, children[1:]))
                                        opts_prompt = ", ".join(map(lambda opt: f"\"{opt}\"", opts))

                                        prompt = f"Answer the following question to the best of your ability from my perspective, based on the information I have given you. If you are unsure of your answer, choose an answer that makes sense for an average person. You have a limited number of choices, and you MUST select one of these choices. The choices are: {opts_prompt}. Use one of these choices exactly. You MUST respond with one of these options. The question is: {question}"
                                        while True:
                                            response = asyncio.run(ChatGPTPrompter.get_response(prompt))
                                            if response in opts:
                                                break

                                        targeted.send_keys(response)

                            try:
                                file_selector = driver.find_element(By.CSS_SELECTOR,
                                                                    "input[id^=jobs-document-upload-file-input-upload-resume]")
                                file_selector.send_keys(os.path.abspath("public/uploads/resume.pdf"))
                            except:
                                pass

                            try:
                                driver.find_element(By.CSS_SELECTOR, "[aria-label=\"Review your application\"]").click()
                                try:
                                    follow_checkbox = driver.find_element(By.ID, "follow-company-checkbox")
                                    if follow_checkbox.get_attribute("checked") == "true":
                                        driver.execute_script("arguments[0].click()", follow_checkbox)
                                except:
                                    pass

                                driver.find_element(By.CSS_SELECTOR, "[aria-label=\"Submit application\"]").click()
                                print(json.dumps(stdout_info))
                                break
                            except:
                                pass

                            driver.find_element(By.CSS_SELECTOR, "[data-easy-apply-next-button]").click()
                            time.sleep(1)
                    except:
                        pass

            time.sleep(3)
            driver.close()

            page_start += 25
            for window_handle in driver.window_handles[:]:
                if window_handle != initial_window_handle:
                    driver.switch_to.window(window_handle)
                    driver.close()
            driver.switch_to.window(initial_window_handle)
            time.sleep(2)
finally:
    driver.quit()
