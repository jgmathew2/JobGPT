import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium_constants import BUFFER_TIME


class WorkdayTextQuestion:
    def __init__(
            self,
            by: By,
            by_selector: str,
            answer: str
    ):
        self.by = by
        self.by_selector = by_selector
        self.answer = answer

    def __call__(self, driver: WebDriver):
        target = self.find_target(driver)
        if not target:
            return

        target.clear()
        time.sleep(BUFFER_TIME)

        target = self.find_target(driver)
        if target:
            target.send_keys(self.answer)

    def find_target(self, driver: WebDriver):
        try:
            return driver.find_element(self.by, self.by_selector)
        except NoSuchElementException:
            return None
