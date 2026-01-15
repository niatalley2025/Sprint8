import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        cls.driver = webdriver.Chrome()

        # Check if the server is reachable before running tests
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

        # ---------------- ROUTE ADDRESSES ----------------

    def test_set_route_addresses(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO

        # ---------------- SUPPORTIVE PLAN ----------------

    def test_select_supportive_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.select_taxi_button()
        page.select_supportive_plan()
        assert page.get_selected_plan() == "Supportive"

        # ---------------- PHONE & SMS ----------------

    def test_fill_phone_number_and_sms_code(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.select_taxi_button()
        page.select_supportive_plan()

        code = page.enter_phone_and_sms_code(data.PHONE_NUMBER)
        assert code is not None
        assert page.get_sms_code() == code

        # ---------------- CREDIT CARD ----------------

    def test_add_credit_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.select_taxi_button()
        page.select_supportive_plan()

        # Enter phone & SMS
        page.enter_phone_and_sms_code(data.PHONE_NUMBER)

        # Payment modal flow
        page.open_payment_modal()
        page.select_add_card()
        page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        page.select_link_card()
        page.close_payment()

        assert page.get_payment_text() == "Card"

        # ---------------- DRIVER COMMENT ----------------

    def test_add_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.select_taxi_button()
        page.select_supportive_plan()
        page.enter_phone_and_sms_code(data.PHONE_NUMBER)

        page.open_payment_modal()
        page.select_add_card()
        page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        page.select_link_card()
        page.close_payment()

        page.add_driver_comment(data.MESSAGE_FOR_DRIVER)
        assert page.get_driver_comment() == data.MESSAGE_FOR_DRIVER

        # ---------------- BLANKET & HANDKERCHIEFS ----------------

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.select_taxi_button()
        page.select_supportive_plan()
        page.enter_phone_and_sms_code(data.PHONE_NUMBER)

        page.open_payment_modal()
        page.select_add_card()
        page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        page.select_link_card()
        page.close_payment()

        page.order_blanket_and_handkerchiefs()
        assert page.blanket_and_handkerchiefs_selected() is True

        # ---------------- ICE CREAM ----------------

    def test_order_two_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.select_taxi_button()
        page.select_supportive_plan()
        page.enter_phone_and_sms_code(data.PHONE_NUMBER)

        page.open_payment_modal()
        page.select_add_card()
        page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        page.select_link_card()
        page.close_payment()

        page.order_ice_cream()
        page.order_ice_cream()
        assert page.get_ice_cream_count() == 2

        # ---------------- TAXI ORDER ----------------

    def test_order_supportive_taxi(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        page.select_taxi_button()
        page.select_supportive_plan()
        page.enter_phone_and_sms_code(data.PHONE_NUMBER)

        page.open_payment_modal()
        page.select_add_card()
        page.add_credit_card(data.CARD_NUMBER, data.CARD_CODE)
        page.select_link_card()
        page.close_payment()
        page.add_driver_comment(data.MESSAGE_FOR_DRIVER)
        page.order_taxi_button_click()
        assert page.verify_car_search_modal()



        # -------- TEARDOWN --------

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()