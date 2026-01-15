import time

from pyexpat.errors import messages
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import helpers


class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # -------- LOCATORS --------
    # Address
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.XPATH, "//button[normalize-space()='Call a taxi']")
    SUPPORTIVE_PLAN_BUTTON = (By.XPATH,"//div[text()='Supportive']")
    SUPPORTIVE_BUTTON = (By.XPATH, "//div[contains(@class,'tcard') and contains(@class,'active') and .//div[normalize-space()='Supportive']]")
    SUPPORTIVE_PLAN_TEXT = (By.XPATH, "//div[@class='tcard-title' and normalize-space()='Supportive']")
    PHONE_BUTTON = (By.XPATH, "//div[contains(@class,'np-button') and .//div[normalize-space()='Phone number']]")
    PHONE_FIELD = (By.ID, 'phone')
    TARIFF_CARD = (By.CLASS_NAME, "tcard")
    SMS_CODE_FIELD = (By.ID, 'code')
    NEXT_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Next']")
    CONFIRM_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Confirm']")
    PAYMENT_METHOD_BUTTON = (By.XPATH, "//div[@class='pp-button filled' and .//div[text()='Payment method']]")
    CURRENT_PAYMENT_METHOD = (By.CLASS_NAME, 'pp-value-text')
    CARD_NUMBER_FIELD = (By.XPATH, "//input[contains(@class,'card-input')]")
    CARD_CVV_FIELD = (By.XPATH, "//div[contains(@class,'card-code-input')]//input[@placeholder='12']")
    LINK_CARD_BUTTON = (By.XPATH, "//button[text()='Link']")
    ADD_CARD_BUTTON = (By.XPATH, "//img[@class='pp-plus' and @alt='plus']")
    CLOSE_PAYMENT_WINDOW = (By.XPATH,'//div[@class="payment-picker open"]//button[@class="close-button section-close"]')
    COMMENT_FIELD = (By.ID, 'comment')
    BLANKET_SLIDER = (By.XPATH, ".//span[contains(@class,'slider')]" )
    BLANKET_CHECKBOX = (By.XPATH, ".//input[@type='checkbox']")
    BLANKET_TOGGLE = (By.XPATH, "//div[contains(@class,'switch')]//span[contains(@class,'slider')]" )
    EXTRA_SECTION = (By.CLASS_NAME, 'reqs-header')
    ICE_CREAM_VALUE = (By.CLASS_NAME, 'counter-value')
    ICE_CREAM_BUTTON = (By.CLASS_NAME, "counter-plus")
    ORDER_TAXI_BUTTON = (By.CLASS_NAME, "smart-button")
    CAR_SEARCH_MODAL = (By.XPATH, "//div[contains(@class,'order-header-content') and .//div[text()='Car search']]")

    def enter_route_adresses(self, from_address, to_address):
        from_input = self.wait.until(
            EC.element_to_be_clickable(self.FROM_FIELD)
        )
        from_input.clear()
        from_input.send_keys(from_address)

        time.sleep(1)  # allow dropdown selection
        # Enter "To" address
        to_input = self.wait.until(
            EC.element_to_be_clickable(self.TO_FIELD)
        )
        to_input.clear()
        to_input.send_keys(to_address)

        time.sleep(1)  # allow route calculation

    def get_from_address(self):
        return self.driver.find_element(*self.FROM_FIELD).get_attribute("value")

    def get_to_address(self):
        return self.driver.find_element(*self.TO_FIELD).get_attribute("value")

    def select_taxi_button(self):
        plan_button = self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON))
        plan_button.click()

    def get_taxi_button(self):
        return self.driver.find_element(*self.CALL_TAXI_BUTTON).text

    def select_supportive_plan(self):
        card_btn = self.wait.until(EC.element_to_be_clickable(self.SUPPORTIVE_PLAN_BUTTON))

        # Check parent div for 'active' class to avoid double click
        parent_card = card_btn.find_element(By.XPATH, "//div[contains(@class,'tcard') and .//div[text()='Supportive']]")
        if "active" not in parent_card.get_attribute("class"):
            card_btn.click()

        # Wait until the card has 'active' class
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@class,'tcard active') and .//div[text()='Supportive']]")))

    def supportive_plan_selected(self):
        try:
            card = self.driver.find_element(
                By.XPATH, "//div[contains(@class,'tcard active') and .//div[text()='Supportive']]"
            )
            return card is not None
        except:
            return False

    def is_tariff_card_visible(self):
        cards = self.wait.until(
            EC.visibility_of_all_elements_located(self.TARIFF_CARD)
        )
        return len(cards) > 0
    # ----------- Phone and SMS -----------
    def fill_phone_number(self, phone_number):
        self.wait.until(
            EC.element_to_be_clickable(self.PHONE_BUTTON)).click()
        phone_input = self.wait.until(
            EC.visibility_of_element_located(self.PHONE_FIELD))
        phone_input.clear()
        phone_input.send_keys(phone_number)
    def fill_sms_code(self, sms_code):
        code_input = self.wait.until(EC.visibility_of_element_located(self.SMS_CODE_FIELD))
        code_input.clear()
        code_input.send_keys(helpers.retrieve_phone_code(self.driver))
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON))
        confirm_btn.click()
        self.wait.until(
            EC.invisibility_of_element(code_input))
    def get_phone_number(self):
        return self.driver.find_element(*self.PHONE_FIELD).get_attribute("value")
    def select_next_button(self):
        return self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON)).click()

    def enter_sms_code(self, code):
        code_input = self.wait.until(EC.element_to_be_clickable(self.SMS_CODE_FIELD))
        code_input.clear()
        code_input.send_keys(code)
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.CONFIRM_BUTTON))
        confirm_btn.click()

    def get_sms_code(self):
        return self.driver.find_element(*self.SMS_CODE_FIELD).text

    # ----------- Credit Card -----------
    def add_credit_card(self, card_number, cvv):
        card_input = self.driver.find_element(*self.CARD_NUMBER_FIELD)
        card_input.clear()
        card_input.send_keys(card_number)

        cvv_input = self.driver.find_element(*self.CARD_CVV_FIELD)
        cvv_input.clear()
        cvv_input.send_keys(cvv)
        # Move focus away to enable Link button
        cvv_input.send_keys(Keys.TAB)
    def select_add_card(self):
        btn = self.driver.find_element(*self.ADD_CARD_BUTTON)
        btn.click()
    def close_payment(self):
        self.driver.find_element(*self.CLOSE_PAYMENT_WINDOW).click()

    def select_link_card(self):

        link_button = self.driver.find_element(*self.LINK_CARD_BUTTON)
        link_button.click()

    def get_payment_method(self):
        self.driver.find_element(*self.PAYMENT_METHOD_BUTTON).click()
    def get_payment_text(self):
        return self.driver.find_element(*self.CURRENT_PAYMENT_METHOD).text

    # ----------- Driver Comment -----------
    def add_driver_comment(self, comment):
        comment_input = self.wait.until(EC.element_to_be_clickable(self.COMMENT_FIELD))
        comment_input.clear()
        comment_input.send_keys(comment)
    def select_add_card2(self):
        return self.driver.find_element(*self.ADD_CARD_BUTTON).click()

    def get_driver_comment(self):
        field = self.wait.until(EC.visibility_of_element_located(self.COMMENT_FIELD))
        return field.get_attribute("value")
    # ----------- Blanket & Handkerchief -----------
    def order_blanket_and_handkerchiefs(self):
        toggle = self.wait.until(EC.element_to_be_clickable(self.BLANKET_TOGGLE))
        toggle.click()
    def blanket_and_handkerchiefs_selected(self):
        checkbox = self.driver.find_element(By.XPATH, "//div[contains(@class,'switch')]//input[@type='checkbox']")
        return checkbox.is_selected()
        return toggle.is_selected() and checkbox.is_selected()
    # ----------- Ice Creams -----------
    def order_ice_cream(self):
        self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_BUTTON)).click()

    def get_ice_cream_count(self):
        value = self.wait.until(EC.visibility_of_element_located(self.ICE_CREAM_VALUE)).text
        return int(value)

    # ----------- Taxi Order -----------
    def order_taxi_button_click(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_TAXI_BUTTON)).click()

    def verify_car_search_modal(self):
        return self.wait.until(EC.visibility_of_element_located(self.CAR_SEARCH_MODAL)).is_displayed()
