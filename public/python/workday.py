import random
import string
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length - 2)) + random.choice(
        string.digits) + random.choice("$!")


driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

BUFFER_TIME = 0.5


def get_unhandled_elements():
    unhandled_elements = []
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

            unhandled_elements.append(element)
        except:
            pass

    return unhandled_elements


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
        sign_in.click()
        time.sleep(BUFFER_TIME)
        try:
            sign_in = driver.find_element(By.CSS_SELECTOR, "[data-automation-id=\"click_filter\"]")
        except:
            break

    time.sleep(10 * BUFFER_TIME)


def do_my_info():
    source_prompt = wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "[data-automation-id-prompt=\"sourcePrompt\"] input")))
    try:
        for x_button in source_prompt.find_element(By.XPATH, "../..").find_elements(By.CSS_SELECTOR,
                                                                                    "[data-automation-id=\"DELETE_charm\"]"):
            x_button.click()
            time.sleep(BUFFER_TIME)
    except:
        pass
    source_prompt.send_keys("LinkedIn")
    time.sleep(BUFFER_TIME)
    source_prompt.send_keys(Keys.ENTER)
    time.sleep(BUFFER_TIME)

    # TODO prev employee?
    prev_employee = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"previousWorker\"]")))
    no_btn = prev_employee.find_element(By.XPATH, "./*[2]").find_element(By.TAG_NAME, "input")
    driver.execute_script("arguments[0].click();", no_btn)
    time.sleep(BUFFER_TIME)

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

    print(len(get_unhandled_elements()))
    if len(get_unhandled_elements()) == 0:
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
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                       "[data-automation-id=\"workExperienceSection\"] [data-automation-id=\"Add\"]"))).send_keys(
                Keys.ENTER)
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
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"workExperience-{i}\"] [data-automation-id=\"location\"]"))).send_keys(
            "Location")

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
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-automation-id=\"educationSection\"] [data-automation-id=\"Add\"]"))).send_keys(
                Keys.ENTER)
        else:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                       "[data-automation-id=\"educationSection\"] [data-automation-id=\"Add Another\"]"))).send_keys(
                Keys.ENTER)

        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"school\"]"))).send_keys(
            "University of Maryland - College Park")
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"degree\"]"))).send_keys(
            "BS")
        field_of_study = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                    f"[data-automation-id=\"education-{i}\"] [data-automation-id-prompt=\"field-of-study\"] input")))
        field_of_study.send_keys("Computer Science")
        time.sleep(BUFFER_TIME)
        field_of_study.send_keys(Keys.ENTER)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"formField-startDate\"] input"))).send_keys(
            "2023")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                   f"[data-automation-id=\"education-{i}\"] [data-automation-id=\"formField-endDate\"] input"))).send_keys(
            "2025")

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
    linked_in = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"linkedinQuestion\"]")))
    linked_in.clear()
    time.sleep(BUFFER_TIME)
    linked_in = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"linkedinQuestion\"]")))
    linked_in.send_keys("https://www.linkedin.com/in/tahmid-zaman-216b51215/")

    print(len(get_unhandled_elements()))
    if len(get_unhandled_elements()) == 0:
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "[data-automation-id=\"bottom-navigation-next-button\"]"))).click()

        # Wait until page not visible
        wait.until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id=\"workExperienceSection\"]")))


def maybe_find(element, by, value):
    try:
        return element.find_element(by, value)
    except:
        return None


def do_questions():
    for question_element in driver.find_elements(By.CSS_SELECTOR,
                                                 "[data-automation-id=\"primaryQuestionnairePage\"] [data-automation-id^=\"formField-\"]"):
        question = question_element.find_element(By.XPATH, "./*[1]").text
        answer_parent = question_element.find_elements(By.XPATH, "./*")[-1]

        answer = maybe_find(answer_parent, By.CSS_SELECTOR, "textarea")
        if answer is not None:
            print(question, "textarea")
        else:
            answer = maybe_find(answer_parent, By.CSS_SELECTOR, "button")
            print(question, "button")
    pass


try:
    driver.get(
        "https://salesforce.wd12.myworkdayjobs.com/en-US/Slack/login?redirect=%2Fen-US%2FSlack%2Fjob%2FTexas---Remote%2FStaff-Software-Engineer--SRE----Slack_JR246676%2Fapply%2FapplyManually")

    do_signin()
    do_my_info()
    do_experience()
    do_questions()

    time.sleep(10_000)
finally:
    driver.quit()
