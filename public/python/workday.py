import asyncio
import json
import os
import re
import time
import urllib.parse
from datetime import datetime
from typing import List

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import ChatGPTPrompter
from selenium_constants import BUFFER_TIME
from state_machine import StateMachine, LinearState, AnswerAIQuestionsState, TransitionAfterAnswer, AIQuestion, \
    AbortDueToErrorState
from workday_question import WorkdayTextQuestion

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 50)


def fix_unhandled_elements():
    for element in driver.find_elements(By.CSS_SELECTOR, "[id^=\"input-\"]"):
        try:
            element_id = element.get_attribute("id")
            label = driver.find_element(By.CSS_SELECTOR, f"[for=\"{element_id}\"]")

            if "*" not in label.text:
                continue

            curr_value = element.get_attribute("value")
            if curr_value is None or curr_value != "":
                continue

            if element.get_attribute("data-automation-id") in ["select-files"]:
                continue

            try:
                parent_element = element.find_element(By.XPATH, "../..")
                if parent_element.get_attribute("data-automation-id") == "multiselectInputContainer":
                    if parent_element.find_element(By.CSS_SELECTOR, "[data-automation-id=\"menuItem\"]"):
                        continue
            except:
                pass

            try:
                response = asyncio.run(ChatGPTPrompter.get_response(
                    f"Answer the following question to the best of your ability from my perspective, based on the information I have given you. If you are unsure of your answer, write N/A. Speak from my perspective, rather than from yours. The question is: {label.text}"))
                element.send_keys(response)
            except:
                pass
        except:
            pass


def do_signin(user_data, exec_data):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"email\"]"))).send_keys(
        exec_data["email"])
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"password\"]"))).send_keys(
        exec_data["password"])
    sign_in = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"click_filter\"]")))
    for _ in range(10):
        try:
            sign_in.click()
            time.sleep(4 * BUFFER_TIME)

            try:
                driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"errorMessage\"]")
                raise SignInException()
            except SignInException:
                raise
            except:
                pass

            sign_in = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"click_filter\"]")
        except SignInException:
            raise
        except:
            break


class SignInException(Exception):
    pass


def do_signup(user_data, exec_data):
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id=\"createAccountLink\"]"))).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"email\"]"))).send_keys(
        exec_data["email"])

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"password\"]"))).send_keys(
        exec_data["password"])
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"verifyPassword\"]"))).send_keys(
        exec_data["password"])
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"createAccountCheckbox\"]"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id=\"click_filter\"]"))).click()

    time.sleep(4 * BUFFER_TIME)

    try:
        driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"errorMessage\"]")
        driver.refresh()
        do_signin(user_data, exec_data)
    except SignInException:
        raise
    except:
        pass


def do_my_info(user_data, exec_data):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"contactInformationPage\"]")))

    try:
        source_prompt = driver.find_element(By.CSS_SELECTOR, "[data-automation-id-prompt=\"sourcePrompt\"] input")
        for x_button in source_prompt.find_element(By.XPATH, "../..").find_elements(By.CSS_SELECTOR,
                                                                                    "[data-automation-id=\"DELETE_charm\"]"):
            x_button.click()
            time.sleep(BUFFER_TIME)

        source_prompt.send_keys("LinkedIn")
        time.sleep(BUFFER_TIME)
        source_prompt = driver.find_element(By.CSS_SELECTOR, "[data-automation-id-prompt=\"sourcePrompt\"] input")
        source_prompt.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
    except:
        pass

    try:
        prev_employee = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"previousWorker\"]")
        no_btn = prev_employee.find_element(By.XPATH, "./*[2]").find_element(By.TAG_NAME, "input")
        driver.execute_script("arguments[0].click();", no_btn)
        time.sleep(BUFFER_TIME)
    except:
        pass

    first_name = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"legalNameSection_firstName\"]")))
    first_name.clear()
    time.sleep(BUFFER_TIME)
    first_name = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"legalNameSection_firstName\"]")))
    first_name.send_keys(user_data["first_name"])
    time.sleep(BUFFER_TIME)
    last_name = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"legalNameSection_lastName\"]")))
    last_name.clear()
    time.sleep(BUFFER_TIME)
    last_name = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"legalNameSection_lastName\"]")))
    last_name.send_keys(user_data["last_name"])
    time.sleep(BUFFER_TIME)

    address_line1 = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_addressLine1\"]")))
    address_line1.clear()
    time.sleep(BUFFER_TIME)
    address_line1 = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_addressLine1\"]")))
    address_line1.send_keys(user_data["address"])
    time.sleep(BUFFER_TIME)
    city = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"addressSection_city\"]")))
    city.clear()
    time.sleep(BUFFER_TIME)
    city = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"addressSection_city\"]")))
    city.send_keys(user_data["city"])
    time.sleep(BUFFER_TIME)
    try:
        county = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"addressSection_regionSubdivision1\"]")
        county.clear()
        time.sleep(BUFFER_TIME)
        county = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_regionSubdivision1\"]")))
        county.send_keys("N/A")
        time.sleep(BUFFER_TIME)
    except:
        pass
    region = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_countryRegion\"]")))
    for c in user_data["state"]:
        region.send_keys(c)
        time.sleep(min(BUFFER_TIME / len(user_data["state"]), 0.1))
    time.sleep(BUFFER_TIME)
    postal_code = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_postalCode\"]")))
    postal_code.clear()
    time.sleep(BUFFER_TIME)
    postal_code = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_postalCode\"]")))
    postal_code.send_keys(user_data["zipcode"])
    time.sleep(BUFFER_TIME)

    phone_number = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"phone-number\"]")))
    phone_number.clear()
    time.sleep(BUFFER_TIME)
    phone_number = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"phone-number\"]")))
    phone_number.send_keys(user_data["phone_number"])
    time.sleep(BUFFER_TIME)

    try:
        driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"formField-phone-device-type\"] button").send_keys(
            "mobile")
        time.sleep(BUFFER_TIME)
    except:
        pass

    fix_unhandled_elements()
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-automation-id=\"bottom-navigation-next-button\"]"))).click()


def do_experience(user_data, exec_data):
    # Wait until page visible
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"workExperienceSection\"]")))

    # Delete (work, education)
    for delete_panel in driver.find_elements(By.CSS_SELECTOR, "[data-automation-id=\"panel-set-delete-button\"]"):
        delete_panel.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)

    # Work
    for i in range(1, len(user_data["job_data"]) + 1):
        job_entry = user_data["job_data"][str(i - 1)]
        if i == 1:
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    "[data-automation-id=\"workExperienceSection\"] [data-automation-id=\"Add\"]").send_keys(
                    Keys.ENTER)
            except:
                pass
        else:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                       "[data-automation-id=\"workExperienceSection\"] [data-automation-id=\"Add Another\"]"))).send_keys(
                Keys.ENTER)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"jobTitle\"]"))).send_keys(
            job_entry["position"])
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"company\"]"))).send_keys(
            job_entry["company"])
        try:
            driver.find_element(By.CSS_SELECTOR,
                                f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"location\"]").send_keys(
                job_entry["location"])
        except:
            pass

        dates = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"dateSectionMonth-input\"]")))
        dates[0].send_keys(job_entry["start_month"] + "/" + job_entry["start_year"])
        dates[0].send_keys(job_entry["end_month"] + "/" + job_entry["end_year"])

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"description\"]"))).send_keys(
            job_entry["description"])

    # Education
    for i in range(1, 2):
        if i == 1:
            try:
                driver.find_element(By.CSS_SELECTOR,
                                    "[data-automation-id=\"educationSection\"] [data-automation-id=\"Add\"]").send_keys(
                    Keys.ENTER)
            except:
                pass
        else:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                       "[data-automation-id=\"educationSection\"] [data-automation-id=\"Add Another\"]"))).send_keys(
                Keys.ENTER)

        try:
            # FRQ form type
            driver.find_element(By.CSS_SELECTOR,
                                f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"school\"]").send_keys(
                user_data["school"])
        except:
            # MCQ form type
            try:
                school_input = driver.find_element(By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"formField-schoolItem\"] input")
                school_input.send_keys(user_data["school"])
                time.sleep(BUFFER_TIME)
                school_input.send_keys(Keys.ENTER)
                time.sleep(BUFFER_TIME)
                driver.switch_to.active_element.send_keys(Keys.ENTER)
            except:
                pass
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"degree\"]"))).send_keys(
            "BS")
        field_of_study = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    f"[data-automation-id=\"education-{i}\"] [data-automation-id-prompt=\"field-of-study\"] input")))
        field_of_study.send_keys(user_data["studying"])
        time.sleep(BUFFER_TIME)
        field_of_study.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        try:
            driver.find_element(By.CSS_SELECTOR,
                                f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"formField-startDate\"] input").send_keys(
                user_data["school_start_year"]
            )
        except:
            pass
        try:
            driver.find_element(By.CSS_SELECTOR,
                                f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"formField-endDate\"] input").send_keys(
                user_data["school_end_year"])
        except:
            pass

    # Skills
    for x_skill in driver.find_elements(By.CSS_SELECTOR,
                                        "[data-automation-id=\"skillsSection\"] [data-automation-id=\"DELETE_charm\"]"):
        try:
            x_skill.click()
        except:
            pass
        time.sleep(BUFFER_TIME)

    skills_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id-prompt=\"skillsPrompt\"] input")))
    
    skill_count = 0
    for skill in user_data["skills"]:
        if skill_count > 5:
            break
        skills_input.send_keys(skill)
        time.sleep(BUFFER_TIME)
        skills_input.send_keys(Keys.ENTER)
        time.sleep(4 * BUFFER_TIME)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)
        skill_count = skill_count + 1

    # Resume
    for x_file in driver.find_elements(By.CSS_SELECTOR, "[data-automation-id=\"delete-file\"]"):
        x_file.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)

    time.sleep(2 * BUFFER_TIME)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"file-upload-input-ref\"]"))).send_keys(
        os.path.abspath("public/uploads/resume.pdf"))
    time.sleep(4 * BUFFER_TIME)

    # LinkedIn
    try:
        linked_in = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"linkedinQuestion\"]")
        linked_in.clear()
        time.sleep(BUFFER_TIME)
        linked_in = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"linkedinQuestion\"]")
        linked_in.send_keys(user_data["linkedin"])
    except:
        pass

    fix_unhandled_elements()
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-automation-id=\"bottom-navigation-next-button\"]"))).click()

    # Wait until page not visible
    wait.until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"workExperienceSection\"]")))


def maybe_find(element, by, value) -> WebElement | None:
    try:
        return element.find_element(by, value)
    except:
        return None


def do_questions(user_data, exec_data):
    # some new questions might pop up as we answer
    seen_ids = []
    while True:
        any_handled = False
        for question_element in driver.find_elements(By.CSS_SELECTOR,
                                                     "[data-automation-id*=\"QuestionnairePage\"] [data-automation-id^=\"formField-\"]"):
            if question_element.id in seen_ids:
                continue

            question = question_element.find_element(By.XPATH, "./*[1]").text
            answer_parent = question_element.find_elements(By.XPATH, "./*")[-1]

            answer = maybe_find(answer_parent, By.CSS_SELECTOR, "textarea")
            if answer is not None:
                try:
                    response = asyncio.run(ChatGPTPrompter.get_response(
                        f"Answer the following question to the best of your ability from my perspective, based on the information I have given you. If you are unsure of your answer, write N/A. Speak from my perspective, rather than from yours. The question is: {question}"))

                    answer.clear()
                    time.sleep(BUFFER_TIME)
                    answer = answer_parent.find_element(By.CSS_SELECTOR, "textarea")
                    answer.send_keys(response)
                except:
                    pass
            else:
                answer = maybe_find(answer_parent, By.CSS_SELECTOR, "button")
                if answer is not None:
                    driver.execute_script("arguments[0].click()", answer)
                    time.sleep(BUFFER_TIME)

                    aria_controls = answer.get_attribute("aria-controls")
                    if aria_controls:
                        try:
                            list_options = driver.find_element(By.ID, aria_controls)
                            children = list_options.find_elements(By.XPATH, "./*")
                            if len(children) > 0:
                                opts = list(map(lambda e: e.text, children[1:]))
                                opts_prompt = ", ".join(map(lambda opt: f"\"{opt}\"", opts))

                                prompt = f"Answer the following question to the best of your ability from my perspective, based on the information I have given you. If you are unsure of your answer, choose an answer that makes sense for an average person. You have a limited number of choices, and you MUST select one of these choices. The choices are: {opts_prompt}. Use one of these choices exactly. You MUST respond with one of these options. The question is: {question}"
                                while True:
                                    response = asyncio.run(ChatGPTPrompter.get_response(prompt))
                                    if response in opts:
                                        break

                                answer.send_keys(response)
                                time.sleep(BUFFER_TIME)
                                answer.send_keys(Keys.ENTER)
                        except:
                            pass

            any_handled = True
            seen_ids.append(question_element.id)
            time.sleep(2 * BUFFER_TIME)

        if not any_handled:
            break
    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id=\"bottom-navigation-next-button\"]"))).click()

    # Handle more questionnare pages, if more exist
    time.sleep(10 * BUFFER_TIME)
    try:
        driver.find_element(By.CSS_SELECTOR, "[data-automation-id*=\"QuestionnairePage\"]")
        do_questions()
    except:
        pass


def do_voluntary(user_data, exec_data):
    buttons = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-automation-id=\"usPersonalInfoSection\"] button")))
    for button in buttons:
        driver.execute_script("arguments[0].click()", button)
        time.sleep(BUFFER_TIME)

        aria_controls = button.get_attribute("aria-controls")
        if aria_controls:
            try:
                button_options = driver.find_element(By.ID, aria_controls)
                children = button_options.find_elements(By.XPATH, "./*")
                if len(children) > 0:
                    ans_found = False
                    for child in children[1:]:
                        child_text = child.text.lower()
                        if "disclose" in child_text or "prefer" in child_text or "wish" in child_text or "decline" in child_text and "hispanic" not in child_text:
                            button.send_keys(child.text)
                            time.sleep(BUFFER_TIME)
                            button.send_keys(Keys.ENTER)
                            ans_found = True
                            break

                    if not ans_found:
                        button.send_keys(children[-1].text)
                        time.sleep(BUFFER_TIME)
                        button.send_keys(Keys.ENTER)
            except:
                pass

    driver.execute_script("arguments[0].click()", wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"agreementCheckbox\"]"))))
    time.sleep(BUFFER_TIME)

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id=\"bottom-navigation-next-button\"]"))).click()


def do_self_identify(user_data, exec_data):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"name\"]"))).send_keys(
        "Abd al-Rahman")
    signature_date = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"dateSectionMonth-display\"]"))).find_element(By.XPATH, "..")
    signature_date.click()
    time.sleep(BUFFER_TIME)
    signature_date.send_keys(datetime.now().strftime("%m/%d/%Y"))
    for element in wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-automation-id=\"disability\"] input"))):
        element_id = element.get_attribute("id")
        label = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f"[for=\"{element_id}\"]")))
        if "want to answer" in label.text.lower():
            driver.execute_script("arguments[0].click()", element)

    wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id=\"bottom-navigation-next-button\"]"))).click()


with open("user_info_table.json") as user_file:
    user_data = json.load(user_file)

with open("public/uploads/WorkDayForm.json") as exec_file:
    exec_data = json.load(exec_file)

with open("public/uploads/filtered_links.txt") as links_file:
    links = [line.rstrip() for line in links_file.readlines()]

if not os.path.exists("public/uploads/link_db.txt"):
    open("public/uploads/link_db.txt", "w").close()

with open("public/uploads/link_db.txt") as link_db:
    used_links = [line.rstrip() for line in link_db.readlines()]

link_db = open("public/uploads/link_db.txt", "a")


class MyInfoState(LinearState):
    def __init__(self, next_state_key: str, driver: WebDriver, user_data):
        super().__init__(next_state_key)
        self.driver = driver
        self.callbacks = [
            WorkdayTextQuestion(By.CSS_SELECTOR, "legalNameSection_firstName", user_data["first_name"]),
            WorkdayTextQuestion(By.CSS_SELECTOR, "legalNameSection_lastName", user_data["last_name"]),
            WorkdayTextQuestion(By.CSS_SELECTOR, "addressSection_addressLine1", user_data["address"]),
            WorkdayTextQuestion(By.CSS_SELECTOR, "addressSection_city", user_data["city"]),
            WorkdayTextQuestion(By.CSS_SELECTOR, "addressSection_regionSubdivision1", "N/A")
        ]

    def do_work(self):
        for callback in self.callbacks:
            callback(self.driver)


class TransitionAfterMyInfo(TransitionAfterAnswer):

    def check_if_error(self, driver: WebDriver) -> bool:
        pass

    def has_page_changed(self) -> bool:
        pass


class MyInfoAIState(AnswerAIQuestionsState):
    def __init__(self, wait: WebDriverWait, error_state_key: str):
        super().__init__(wait)
        self.error_state_key = error_state_key

    def find_unanswered_questions(self) -> List[AIQuestion]:
        pass

    def submit_page(self):
        pass

    def create_transition_worker(self) -> TransitionAfterAnswer:
        return TransitionAfterMyInfo(
            self.error_state_key
        )


class ExperienceState(LinearState):
    def __init__(self, next_state_key: str, driver: WebDriver):
        super().__init__(next_state_key)
        self.driver = driver

    def do_work(self):
        for delete_panel in self.driver.find_elements(By.CSS_SELECTOR, "[data-automation-id=\"panel-set-delete-button\"]"):
            delete_panel.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)

        for x_skill in driver.find_elements(By.CSS_SELECTOR,
                                            "[data-automation-id=\"skillsSection\"] [data-automation-id=\"DELETE_charm\"]"):
            try:
                x_skill.click()
            except:
                pass
        time.sleep(BUFFER_TIME)


try:
    for link in links:
        if link in used_links:
            continue

        try:
            driver.get(link)
            position_name = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"jobPostingHeader\"]"))).text
            position_company = "Unknown"
            try:
                current_url = urllib.parse.urlparse(driver.current_url)
                match_result = re.search(r"(.*)\.wd(.*)\.myworkdayjobs\.com", current_url.hostname)
                if match_result:
                    position_company = match_result.group(1)
            except:
                pass

            wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-uxi-element-id^=\"Apply_adventureButton\"]"))).click()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id=\"applyManually\"]"))).click()

            do_signup(user_data, exec_data)
            time.sleep(10 * BUFFER_TIME)
            states = {
                "Error": AbortDueToErrorState(),
                "My Info / Main": MyInfoState("My Info / AI", driver, user_data),
                "My Info / AI": MyInfoAIState(wait, "Error"),
                "Experience / Main": ExperienceState("Experience / Answer", driver)
            }
            initial_state = None
            state_machine = StateMachine(states, initial_state)
            state_machine.run()
            do_my_info(user_data, exec_data)
            do_experience(user_data, exec_data)
            do_questions(user_data, exec_data)
            do_voluntary(user_data, exec_data)
            do_self_identify(user_data, exec_data)

            used_links.append(link)

            try:
                link_db.write(link)
                link_db.write("\n")
                link_db.flush()
            except:
                pass

            print(json.dumps([position_name, position_company]))
            time.sleep(5)
        except:
            pass
finally:
    driver.quit()