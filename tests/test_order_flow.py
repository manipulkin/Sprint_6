# Позитивный сценарий оформления заказа — до появления окна «Заказ оформлен»

import allure
#ПРАВКА параметризация была заменена двумя независимыми тестами

from pages.main_page import MainPage   
from pages.order_page import OrderPage
from config.data import CUSTOMER_AKAKIY, CUSTOMER_AGAFYA   


@allure.parent_suite("Тесты оформления заказа")  # верхний уровень в разделе «Сюиты»
@allure.title("Позитивный сценарий заказа")   # отображается вместо имени класса
@allure.feature("Оформление заказа")    # группировка в разделе «Категории»
@allure.story("Позитивный сценарий")   # подгруппа внутри «Категорий»

# Проверка оформления заказа
class TestOrderHappyPath:

    @allure.title("Оформление заказа через верхнюю кнопку «Заказать» (клиент Акакий)")
    def test_order_from_top_button(self, driver):
        main = MainPage(driver)
        order = OrderPage(driver)
        customer = CUSTOMER_AKAKIY

        with allure.step("Главная страница"):
            main.open()
            main.accept_cookies_if_shown()

        with allure.step("Перейти к форме заказа через верхнюю кнопку «Заказать»"):
            main.click_order_top()

        with allure.step("Шаг 1 формы — личные данные и метро"):
            order.fill_personal_data(
                customer["first_name"],
                customer["last_name"],
                customer["address"],
                customer["phone"],
            )
            order.select_metro(customer["metro"])

        with allure.step("Шаг 2 формы — дата, срок, цвет"):
            order.click_next()
            order.fill_rent_details(
                customer["date"],
                customer["period"],
                customer["color"],
            )

        with allure.step("Отправить заказ"):
            order.submit_order()

        with allure.step("Проверить попап «Заказ оформлен»"):
            order.wait_success_modal()

        with allure.step("Закрыть попап и убедиться, что перешли на страницу трекера"):
            order.close_success_modal_and_wait()
            order.wait_for_track_page()
            assert "/track" in order.get_current_url(), "Не удалось перейти на страницу трекера заказа"

    @allure.title("Оформление заказа через нижнюю кнопку «Заказать» (клиент Агафья)")
    def test_order_from_bottom_button(self, driver):
        main = MainPage(driver)
        order = OrderPage(driver)
        customer = CUSTOMER_AGAFYA

        with allure.step("Главная страница"):
            main.open()
            main.accept_cookies_if_shown()

        with allure.step("Перейти к форме заказа через нижнюю кнопку «Заказать»"):
            main.click_order_bottom()

        with allure.step("Шаг 1 формы — личные данные и метро"):
            order.fill_personal_data(
                customer["first_name"],
                customer["last_name"],
                customer["address"],
                customer["phone"],
            )
            order.select_metro(customer["metro"])

        with allure.step("Шаг 2 формы — дата, срок, цвет"):
            order.click_next()
            order.fill_rent_details(
                customer["date"],
                customer["period"],
                customer["color"],
            )

        with allure.step("Отправить заказ"):
            order.submit_order()

        with allure.step("Проверить попап «Заказ оформлен»"):
            order.wait_success_modal()

        with allure.step("Закрыть попап и убедиться, что перешли на страницу трекера"):
            order.close_success_modal_and_wait()
            order.wait_for_track_page()
            assert "/track" in order.get_current_url(), "Не удалось перейти на страницу трекера заказа"
