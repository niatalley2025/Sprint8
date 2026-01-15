import data
import helpers
from selenium import webdriver
from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        from selenium.webdriver import DesiredCapabilities

        # Enable Chrome logging for SMS retrieval
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        cls.driver = webdriver.Chrome()

        # Ensure server is reachable
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            raise Exception("Urban Routes server is not reachable")

        cls.driver.get(data.URBAN_ROUTES_URL)
        cls.page = UrbanRoutesPage(cls.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # ---------- TESTS ----------

    def test_set_address(self):
        self.page.set_address("Downtown", "Airport")

    def test_select_supportive_plan(self):
        self.page.select_supportive_plan()

    def test_fill_phone_number_and_confirm(self):
        self.page.fill_phone_number_and_confirm("5551234567")

    def test_add_credit_card(self):
        self.page.add_credit_card("4111111111111111", "123")

    def test_add_driver_comment(self):
        self.page.add_driver_comment("Please call on arrival")

    def test_order_blanket_and_handkerchiefs(self):
        self.page.order_blanket_and_handkerchiefs()

    def test_order_2_ice_creams(self):
        self.page.order_ice_creams(2)

    def test_order_taxi_with_supportive_plan(self):
        self.page.order_taxi_with_supportive_plan("Please call when arriving")