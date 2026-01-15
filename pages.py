
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import helpers


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

        # -------- LOCATORS --------

    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[normalize-space()='Call a taxi']")
    SUPPORTIVE_PLAN_BUTTON = (By.XPATH, "//div[text()='Supportive']")
    SUPPORTIVE_PLAN_TEXT = (By.XPATH, "//div[@class='tcard-title' and normalize-space()='Supportive']")
    PHONE_FIELD = (By.ID, "phone")
    PHONE_BUTTON = (By.XPATH, "//div[@class='np-button' and .//div[text()='Phone number']]")
    SMS_CODE_FIELD = (By.ID, "code")
    NEXT_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Next']")
    CONFIRM_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Confirm']")
    PAYMENT_METHOD_BUTTON = (By.XPATH, "//div[@class='pp-button filled' and .//div[text()='Payment method']]")
    CURRENT_PAYMENT_METHOD = (By.CLASS_NAME, "pp-value-text")
    ADD_CARD_BUTTON = (By.XPATH, "//img[@class='pp-plus' and @alt='plus']")
    CARD_NUMBER_FIELD = (By.XPATH, "//input[contains(@class,'card-input')]")
    CARD_CVV_FIELD = (By.XPATH, "//div[contains(@class,'card-code-input')]//input[@placeholder='12']")
    LINK_CARD_BUTTON = (By.XPATH, "//button[text()='Link']")
    CLOSE_PAYMENT_WINDOW = (By.XPATH,
                            '//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    COMMENT_FIELD = (By.ID, "comment")
    BLANKET_TOGGLE = (By.XPATH, "//div[contains(@class,'switch')]//span[contains(@class,'slider')]")
    BLANKET_CHECKBOX = (By.XPATH, "//div[contains(@class,'switch')]//input[@type='checkbox']")
    ICE_CREAM_BUTTON = (By.CLASS_NAME, "counter-plus")
    ICE_CREAM_VALUE = (By.CLASS_NAME, "counter-value")
    ORDER_TAXI_BUTTON = (By.CLASS_NAME, "smart-button")
    CAR_SEARCH_MODAL = (By.XPATH, "//div[contains(@class,'order-header-content') and .//div[text()='Car search']]")

    # -------- HELPER METHODS --------
    def wait_for_element_interactable(self, locator):
        """Poll until the element is displayed and enabled for interaction."""
        for _ in range(20):
            element = self.driver.find_element(*locator)
            if element.is_displayed() and element.is_enabled():
                return element
        raise Exception(f"Element not interactable: {locator}")

    # -------- ROUTE METHODS --------
    def enter_route_adresses(self, from_address, to_address):
        from_input = self.wait_for_element_interactable(self.FROM_FIELD)
        from_input.clear()
        from_input.send_keys(from_address)

        to_input = self.wait_for_element_interactable(self.TO_FIELD)
        to_input.clear()
        to_input.send_keys(to_address)

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_FIELD).get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(*self.TO_FIELD).get_attribute("value")

    # -------- PLAN METHODS --------
    def select_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_supportive_plan(self):
        self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_BUTTON)).click()


    def get_selected_plan(self):
        return self.driver.find_element(*self.SUPPORTIVE_PLAN_TEXT).text

    # -------- PHONE & SMS METHODS --------
    def enter_phone_and_sms_code(self, phone_number):
        # Click phone input
        self.wait_for_element_interactable(self.PHONE_BUTTON).click()

        # Enter phone number
        phone_input = self.wait_for_element_interactable(self.PHONE_FIELD)
        phone_input.clear()
        phone_input.send_keys(phone_number)

        # Click next
        self.wait_for_element_interactable(self.NEXT_BUTTON).click()

        # Retrieve SMS code
        code = helpers.retrieve_phone_code(self.driver)

        # Enter code in field
        code_input = self.wait_for_element_interactable(self.SMS_CODE_FIELD)
        code_input.clear()
        code_input.send_keys(code)

        # Click confirm
        self.wait_for_element_interactable(self.CONFIRM_BUTTON).click()
        return code

    def get_phone_number(self):
        return self.driver.find_element(*self.PHONE_FIELD).get_attribute("value")

    def get_sms_code(self):
        return self.driver.find_element(*self.SMS_CODE_FIELD).get_attribute("value")

    # -------- PAYMENT METHODS --------
    def open_payment_modal(self):
        self.wait_for_element_interactable(self.PAYMENT_METHOD_BUTTON).click()

    def select_add_card(self):
        self.wait_for_element_interactable(self.ADD_CARD_BUTTON).click()

    def add_credit_card(self, number, cvv):
        num_field = self.wait_for_element_interactable(self.CARD_NUMBER_FIELD)
        num_field.clear()
        num_field.send_keys(number)

        cvv_field = self.wait_for_element_interactable(self.CARD_CVV_FIELD)
        cvv_field.clear()
        cvv_field.send_keys(cvv)
        cvv_field.send_keys(Keys.TAB)

    def select_link_card(self):
        self.wait_for_element_interactable(self.LINK_CARD_BUTTON).click()

    def close_payment(self):
        self.wait_for_element_interactable(self.CLOSE_PAYMENT_WINDOW).click()

    def get_payment_text(self):
        return self.driver.find_element(*self.CURRENT_PAYMENT_METHOD).text

    # -------- DRIVER COMMENT --------
    def add_driver_comment(self, comment):
        comment_input = self.wait_for_element_interactable(self.COMMENT_FIELD)
        comment_input.clear()
        comment_input.send_keys(comment)

    def get_driver_comment(self):
        return self.driver.find_element(*self.COMMENT_FIELD).get_attribute("value")

    # -------- BLANKET & HANDKERCHIEFS --------
    def order_blanket_and_handkerchiefs(self):
        self.wait_for_element_interactable(self.BLANKET_TOGGLE).click()

    def blanket_and_handkerchiefs_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).is_selected()

    # -------- ICE CREAM --------
    def order_ice_cream(self):
        self.wait_for_element_interactable(self.ICE_CREAM_BUTTON).click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_VALUE).text)

    # -------- TAXI ORDER --------
    def order_taxi_button_click(self):
        self.wait_for_element_interactable(self.ORDER_TAXI_BUTTON).click()

    def verify_car_search_modal(self):
        return self.driver.find_element(*self.CAR_SEARCH_MODAL).is_displayed()