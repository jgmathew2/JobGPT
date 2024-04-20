import asyncio
from datetime import datetime
import random
import string
import time
import ChatGPTPrompter

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length - 2)) + random.choice(
        string.digits) + random.choice("$!")


driver = webdriver.Firefox()
wait = WebDriverWait(driver, 1000)

BUFFER_TIME = 0.5


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


def do_signup():
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id=\"createAccountLink\"]"))).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"email\"]"))).send_keys(
        "abdalrahmanumayyad@gmail.com")

    password = generate_random_string(8)
    print(password)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"password\"]"))).send_keys(
        password)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"verifyPassword\"]"))).send_keys(
        password)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"createAccountCheckbox\"]"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id=\"click_filter\"]"))).click()


def do_signin():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"email\"]"))).send_keys(
        "abdalrahmanumayyad@gmail.com")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"password\"]"))).send_keys(
        "VzxwuY7$")
    sign_in = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"click_filter\"]")))
    for _ in range(10):
        try:
            sign_in.click()
            time.sleep(4 * BUFFER_TIME)
            sign_in = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"click_filter\"]")
        except:
            break

    time.sleep(10 * BUFFER_TIME)


def do_my_info():
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
    first_name.send_keys("Abd al-Rahman")
    time.sleep(BUFFER_TIME)
    last_name = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"legalNameSection_lastName\"]")))
    last_name.clear()
    time.sleep(BUFFER_TIME)
    last_name = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"legalNameSection_lastName\"]")))
    last_name.send_keys("Umayyad")
    time.sleep(BUFFER_TIME)

    address_line1 = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_addressLine1\"]")))
    address_line1.clear()
    time.sleep(BUFFER_TIME)
    address_line1 = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_addressLine1\"]")))
    address_line1.send_keys("8097 La Plata Drive")
    time.sleep(BUFFER_TIME)
    city = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"addressSection_city\"]")))
    city.clear()
    time.sleep(BUFFER_TIME)
    city = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"addressSection_city\"]")))
    city.send_keys("College Park")
    time.sleep(BUFFER_TIME)
    try:
        county = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"addressSection_regionSubdivision1\"]")
        county.clear()
        time.sleep(BUFFER_TIME)
        county = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"addressSection_regionSubdivision1\"]")))
        county.send_keys("N/A")
        time.sleep(BUFFER_TIME)
    except:
        pass
    region = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_countryRegion\"]")))
    for c in "Maryland":
        region.send_keys(c)
        time.sleep(min(BUFFER_TIME / len("Maryland"), 0.1))
    time.sleep(BUFFER_TIME)
    postal_code = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_postalCode\"]")))
    postal_code.clear()
    time.sleep(BUFFER_TIME)
    postal_code = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id=\"addressSection_postalCode\"]")))
    postal_code.send_keys("20742")
    time.sleep(BUFFER_TIME)

    phone_number = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"phone-number\"]")))
    phone_number.clear()
    time.sleep(BUFFER_TIME)
    phone_number = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"phone-number\"]")))
    phone_number.send_keys("(301) 405-1000")
    time.sleep(BUFFER_TIME)

    try:
        driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"formField-phone-device-type\"] button").send_keys("mobile")
        time.sleep(BUFFER_TIME)
    except:
        pass

    fix_unhandled_elements()
    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "[data-automation-id=\"bottom-navigation-next-button\"]"))).click()


def do_experience():
    # Wait until page visible
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"workExperienceSection\"]")))

    # Delete (work, education)
    for delete_panel in driver.find_elements(By.CSS_SELECTOR, "[data-automation-id=\"panel-set-delete-button\"]"):
        delete_panel.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)

    # Work
    for i in range(1, 2):
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
            "Job Title")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"company\"]"))).send_keys(
            "Company")
        try:
            driver.find_element(By.CSS_SELECTOR, f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"location\"]").send_keys("Location")
        except:
            pass

        dates = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                                f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"dateSectionMonth-input\"]")))
        dates[0].send_keys("09/2022")
        dates[1].send_keys("05/2023")

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"description\"]"))).send_keys(
            "Description")

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
                "University of Maryland - College Park")
        except:
            # MCQ form type
            try:
                school_input = driver.find_element(By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"formField-schoolItem\"] input")
                school_input.send_keys("University of Maryland - College Park")
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
        field_of_study.send_keys("Computer Science")
        time.sleep(BUFFER_TIME)
        field_of_study.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        try:
            driver.find_element(By.CSS_SELECTOR, f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"formField-startDate\"] input").send_keys("2023")
        except:
            pass
        try:
            driver.find_element(By.CSS_SELECTOR, f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"formField-endDate\"] input").send_keys("2025")
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
    for skill in ["java", "python", "c++"]:
        skills_input.send_keys(skill)
        time.sleep(BUFFER_TIME)
        skills_input.send_keys(Keys.ENTER)
        time.sleep(4 * BUFFER_TIME)
        driver.switch_to.active_element.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)

    # Resume
    for x_file in driver.find_elements(By.CSS_SELECTOR, "[data-automation-id=\"delete-file\"]"):
        x_file.send_keys(Keys.ENTER)
        time.sleep(BUFFER_TIME)

    time.sleep(2 * BUFFER_TIME)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"file-upload-input-ref\"]"))).send_keys(
        "/home/tfz/Downloads/athlete.pdf")
    time.sleep(4 * BUFFER_TIME)

    # LinkedIn
    try:
        linked_in = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"linkedinQuestion\"]")
        linked_in.clear()
        time.sleep(BUFFER_TIME)
        linked_in = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"linkedinQuestion\"]")
        linked_in.send_keys("https://www.linkedin.com/in/tahmid-zaman-216b51215/")
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


def do_questions():
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


def do_voluntary():
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


def do_self_identify():
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


try:
    driver.get(
        "https://santander.wd3.myworkdayjobs.com/en-US/SantanderCareers/login?redirect=%2Fen-US%2FSantanderCareers%2Fjob%2FMiami%2FIntern-CSU-CAC_Req1300250-1%2Fapply%2FapplyManually")

    do_signin()
    do_my_info()
    do_experience()
    do_questions()
    do_voluntary()
    do_self_identify()

    time.sleep(10_000)
finally:
    driver.quit()
