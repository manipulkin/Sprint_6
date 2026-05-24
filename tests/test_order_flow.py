# Позитивный сценарий оформления заказа — до появления окна «Заказ оформлен»

import allure
import pytest

from pages.main_page import MainPage
from pages.order_page import OrderPage
# ИСПРАВЛЕНО: импортируем ORDER_CASES — список данных для параметризации
from config.data import ORDER_CASES


@allure.parent_suite("Тесты оформления заказа")
@allure.feature("Оформление заказа")
@allure.story("Позитивный сценарий")
class TestOrderHappyPath:

    @pytest.mark.parametrize(
        "is_header, customer",
        ORDER_CASES,
        ids=["Верхняя_кнопка", "Нижняя_кнопка"],
    )
    @allure.title("Оформление заказа: верхняя и нижняя кнопки «Заказать»")
    @allure.description(
        "Параметризованный тест проверяет полный флоу заказа "
        "для двух точек входа и двух наборов данных"
    )
    def test_successful_order(self, driver, is_header, customer):
        main = MainPage(driver)
        order = OrderPage(driver)

        with allure.step("Открыть главную страницу и принять cookies"):
            main.open()
            main.accept_cookies_if_shown()

        with allure.step("Перейти к форме заказа"):
            # if отсутствует — логика выбора кнопки внутри go_to_order()
            main.go_to_order(is_header=is_header)

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
            assert "/track" in order.get_current_url(), (
                "Не удалось перейти на страницу трекера заказа"
            )
