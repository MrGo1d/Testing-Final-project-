from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .locators import BasePageLocators
import math


class BasePage():
    def __init__(self, browser, url, timeout=10):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def go_to_basket_page(self):
            """method finds the basket link by CSS selectors and click it"""
            link = self.browser.find_element(*BasePageLocators.BASKET_LINK)
            link.click()

    def go_to_login_page(self):
        """method finds the login link by CSS selectors and click it"""
        link = self.browser.find_element(*BasePageLocators.LOGIN_LINK)
        link.click()

    def is_disappeared(self, how, what, timeout=4):
        """method checks that element will disappeare at page in {timeout} time"""
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException).\
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def is_element_present(self, how, what):
        """is the element presented on page method checks"""
        try:
            self.browser.find_element(how, what)
        except NoSuchElementException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        """method checks that element will not present at page in {timeout} time"""
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True
        return False

    def open(self):
        """method open a browser"""
        self.browser.get(self.url)

    def should_be_authorized_user(self):
        """is user authorized method checks"""
        assert self.is_element_present(*BasePageLocators.USER_ICON), "User icon is not presented," \
                                                                 " probably unauthorised user"
        
    def should_be_login_link(self):
        """method checks that login link presents on the base page"""
        assert self.is_element_present(*BasePageLocators.LOGIN_LINK), "Login link is not presented"

    def solve_quiz_and_get_code(self):
        """method for solving the task and sending the result"""
        alert = self.browser.switch_to.alert
        x = alert.text.split(" ")[2]
        answer = str(math.log(abs((12 * math.sin(float(x))))))
        alert.send_keys(answer)
        alert.accept()
        try:
            alert = self.browser.switch_to.alert
            alert_text = alert.text
            print(f"Your code: {alert_text}")
            alert.accept()
        except NoAlertPresentException:
            print("No second alert presented")
    