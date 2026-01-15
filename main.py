import data
import helpers
import pages
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

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = pages.UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO
        page.select_taxi_button()
        assert page.get_taxi_button() == 'Call a taxi'
        page.select_supportive_plan()
        assert page.supportive_plan_selected()

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = pages.UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO
        page.select_taxi_button()
        assert page.is_tariff_card_visible()
        page.select_supportive_plan()
        assert page.supportive_plan_selected()
        page.fill_phone_number('+1 7709011647')
        assert page.get_phone_number() == '+1 7709011647', "Phone number is wrong"
        page.select_next_button()
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None
        page.get_sms_code()
        assert page.get_phone_number() == '+1 7709011647', "Phone number is wrong"


    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = pages.UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO
        page.select_taxi_button()
        assert page.is_tariff_card_visible()
        page.select_supportive_plan()
        assert page.supportive_plan_selected()
        page.fill_phone_number('+1 7709011647')
        assert page.get_phone_number() == '+1 7709011647', "Phone number is wrong"
        page.select_next_button()
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None
        page.enter_sms_code(code)
        page.get_payment_method()
        page.select_add_card()
        page.add_credit_card('12345678901', '12')
        page.select_link_card()
        page.close_payment()
        payment_text = page.get_payment_text()
        assert "Card" == payment_text




    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = pages.UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO
        page.select_taxi_button()
        assert page.is_tariff_card_visible()
        page.select_supportive_plan()
        assert page.supportive_plan_selected()
        page.fill_phone_number('+1 7709011647')
        assert page.get_phone_number() == '+1 7709011647', "Phone number is wrong"
        page.select_next_button()
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None
        page.enter_sms_code(code)
        page.get_payment_method()
        page.select_add_card()
        page.add_credit_card('12345678901', '12')
        page.select_link_card()
        page.close_payment()
        payment_text = page.get_payment_text()
        assert "Card" == payment_text
        page.add_driver_comment(data.MESSAGE_FOR_DRIVER)
        comment = page.get_driver_comment()
        assert comment == data.MESSAGE_FOR_DRIVER

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = pages.UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO
        page.select_taxi_button()
        assert page.is_tariff_card_visible()
        page.select_supportive_plan()
        assert page.supportive_plan_selected()
        page.fill_phone_number('+1 7709011647')
        assert page.get_phone_number() == '+1 7709011647', "Phone number is wrong"
        page.select_next_button()
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None
        page.enter_sms_code(code)
        page.get_payment_method()
        page.select_add_card()
        page.add_credit_card('12345678901', '12')
        page.select_link_card()
        page.close_payment()
        payment_text = page.get_payment_text()
        assert "Card" == payment_text
        page.add_driver_comment(data.MESSAGE_FOR_DRIVER)
        comment = page.get_driver_comment()
        assert comment == data.MESSAGE_FOR_DRIVER
        page.order_blanket_and_handkerchiefs()
        assert page.blanket_and_handkerchiefs_selected(), "Blanket and Handkerchiefs were not selected"


    def test_order_2_ice_creams(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = pages.UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO
        page.select_taxi_button()
        assert page.is_tariff_card_visible()
        page.select_supportive_plan()
        assert page.supportive_plan_selected()
        page.fill_phone_number('+1 7709011647')
        assert page.get_phone_number() == '+1 7709011647', "Phone number is wrong"
        page.select_next_button()
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None
        page.enter_sms_code(code)
        page.get_payment_method()
        page.select_add_card()
        page.add_credit_card('12345678901', '12')
        page.select_link_card()
        page.close_payment()
        payment_text = page.get_payment_text()
        assert "Card" == payment_text
        page.add_driver_comment(data.MESSAGE_FOR_DRIVER)
        comment = page.get_driver_comment()
        assert comment == data.MESSAGE_FOR_DRIVER
        page.order_blanket_and_handkerchiefs()
        assert page.blanket_and_handkerchiefs_selected(), "Blanket and Handkerchiefs were not selected"
        for _ in range(2):
            page.order_ice_cream()
        ice_cream_count = page.get_ice_cream_count()
        assert ice_cream_count == 2

    def test_order_taxi_supportive(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = pages.UrbanRoutesPage(self.driver)
        page.enter_route_adresses(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from_address() == data.ADDRESS_FROM
        assert page.get_to_address() == data.ADDRESS_TO
        page.select_taxi_button()
        assert page.is_tariff_card_visible()
        page.select_supportive_plan()
        assert page.supportive_plan_selected()
        page.fill_phone_number('+1 7709011647')
        assert page.get_phone_number() == '+1 7709011647', "Phone number is wrong"
        page.select_next_button()
        code = helpers.retrieve_phone_code(self.driver)
        assert code is not None
        page.enter_sms_code(code)
        page.get_payment_method()
        page.select_add_card()
        page.add_credit_card('12345678901', '12')
        page.select_link_card()
        page.close_payment()
        payment_text = page.get_payment_text()
        assert "Card" == payment_text
        page.add_driver_comment(data.MESSAGE_FOR_DRIVER)
        comment = page.get_driver_comment()
        assert comment == data.MESSAGE_FOR_DRIVER
        page.order_blanket_and_handkerchiefs()
        assert page.blanket_and_handkerchiefs_selected(), "Blanket and Handkerchiefs were not selected"
        for _ in range(2):
            page.order_ice_cream()
        ice_cream_count = page.get_ice_cream_count()
        assert ice_cream_count == 2
        page.order_taxi_button_click()
        assert page.verify_car_search_modal()
