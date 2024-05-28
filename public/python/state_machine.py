from typing import Callable, Dict, List
from abc import ABC, abstractmethod

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

DONE_STATE_KEY = "Done"


class MachineState(ABC):

    @abstractmethod
    def next_state(self) -> str:
        pass


class LinearState(MachineState):
    def __init__(self, next_state_key):
        self.next_state_key = next_state_key

    def next_state(self) -> str:
        self.do_work()
        return self.next_state_key

    @abstractmethod
    def do_work(self):
        pass


class StateMachine:
    def __init__(self, states: Dict[str, MachineState], initial_state: MachineState):
        self.states = states
        self.current_state = initial_state

    def run(self):
        while True:
            next_state_key = self.current_state.next_state()
            if next_state_key == DONE_STATE_KEY:
                break

            self.current_state = self.states[next_state_key]


class AIQuestion(ABC):
    @abstractmethod
    def answer(self):
        pass


class TransitionAfterAnswer(ABC):
    def __init__(self, error_state_key: str, transitions: List[tuple[Callable[[WebDriver], bool], str]]):
        self.error_state_key = error_state_key
        self.transitions = transitions
        self.on_original_page = False

    def find_next_state_key(self, driver: WebDriver) -> str | False:
        if self.check_if_error(driver):
            return self.error_state_key

        if self.on_original_page and self.has_page_changed():
            self.on_original_page = False

        if not self.on_original_page:
            for callback, next_state_key in self.transitions:
                if callback(driver):
                    return next_state_key

        return False

    @abstractmethod
    def check_if_error(self, driver: WebDriver) -> bool:
        pass

    @abstractmethod
    def has_page_changed(self) -> bool:
        pass


class AnswerAIQuestionsState(MachineState):
    def __init__(self, wait: WebDriverWait):
        self.wait = wait

    def next_state(self) -> str:
        while True:
            unanswered_questions = self.find_unanswered_questions()
            if len(unanswered_questions) == 0:
                break

            for question in unanswered_questions:
                question.answer()

        self.submit_page()

        transition_worker = self.create_transition_worker()
        return self.wait.until(lambda driver: transition_worker.find_next_state_key(driver))

    @abstractmethod
    def find_unanswered_questions(self) -> List[AIQuestion]:
        pass

    @abstractmethod
    def submit_page(self):
        pass

    @abstractmethod
    def create_transition_worker(self) -> TransitionAfterAnswer:
        pass


# TODO: create a state that allows you to yield control back to the user
class AbortDueToErrorState(MachineState):
    def next_state(self) -> str:
        raise Exception("Unhandled error")
