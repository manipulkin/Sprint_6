# Позитивный сценарий оформления заказа до конца и проверки логотипов
# Задумка с параметрами такая: сначала проверяем верхнюю «Заказать» и данные Акакия, а потом проверяем нижнюю «Заказать» и данные Агафьи

import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.main_page import MainPage
from pages.order_page import OrderPage


@allure.parent_suite("Тесты оформления заказа")  # вместо имени файла test_order_flow
@allure.title("Позитивный сценарий заказа")       # вместо имени класса TestOrderHappyPath
@allure.feature("Оформление заказа")              # группировка в разделе «Категории»
@allure.story("Позитивный сценарий")              # подгруппа внутри
class TestOrderHappyPath:

    # Первый набор данных: клиент Акакий, верхняя кнопка «Заказать»
    CUSTOMER_AKAKIY = {
        "first_name": "Акакий",
        "last_name": "Огурцов",
        "phone": "+79998884545",
        "metro": "Черкизовская",
        "address": "г. Москва, ул. Тестовая, д. 1",
        "date": "01.12.2026",
        "period": "сутки",
        "color": "чёрный",
    }

    # Второй набор данных: клиентка Агафья, нижняя кнопка «Заказать»
    CUSTOMER_AGAFYA = {
        "first_name": "Агафья",
        "last_name": "Ручковна",
        "phone": "+79031234567",
        "metro": "Сокольники",
        "address": "г. Москва, ул. Примерная, д. 2",
        "date": "05.12.2026",
        "period": "двое суток",
        "color": "серый",
    }

    @pytest.mark.parametrize(
        "use_bottom_entry, customer",
        [
            pytest.param(False, CUSTOMER_AKAKIY, id="header_button_akkakiy"),  # False = верхняя кнопка
            pytest.param(True,  CUSTOMER_AGAFYA, id="footer_button_agafya"),   # True  = нижняя кнопка
        ],
    )
    @allure.title("Тестирование заказа самоката")
    def test_positive_order_flow_logos_and_success_modal(
        self,
        driver,
        use_bottom_entry,
        customer,
    ):
        # Добавляем параметры в Allure-отчёт чтобы было видно в каждом прогоне теста
        entry_label = "Нижняя «Заказать»" if use_bottom_entry else "Верхняя «Заказать»"
        allure.dynamic.parameter("Точка входа", entry_label)                            # какая кнопка использовалась
        allure.dynamic.parameter("Клиент", f"{customer['first_name']} {customer['last_name']}")  # чьи данные в тесте

        main  = MainPage(driver)
        order = OrderPage(driver)

        wait = WebDriverWait(driver, 20)  # ждем 20 сек

        with allure.step("Главная страница"):
            main.open()                     # открываем стенд
            main.accept_cookies_if_shown()  # убираем баннер куки, если он появился

        with allure.step("Перейти к форме заказа"):
            if use_bottom_entry:
                main.click_order_bottom()  # нижняя кнопка: прокручиваем, избавляемся от шапки и кликаем
            else:
                main.click_order_top()     # верхняя кнопка: тут просто клик, тк шапка не мешает

        with allure.step("Шаг 1 формы — личные данные и метро"):
            order.fill_personal_data(       # заполняем данные
                customer["first_name"],
                customer["last_name"],
                customer["address"],
                customer["phone"],
            )
            order.select_metro(customer["metro"])  # вводим станцию метро и выбираем из выпадашки

        with allure.step("Шаг 2 формы — дата, срок, цвет"):
            order.click_next()  # переходим на шаг 2, кнопка активна только при корректно заполненном шаге 1
            order.fill_rent_details(        # заполняем данные
                customer["date"],
                customer["period"],
                customer["color"],
            )

        with allure.step("Отправить заказ"):
            order.submit_order()  # кликаем «Заказать», затем «Да» для подтверждения

        with allure.step("Проверить попап «Заказ оформлен»"):
            order.wait_success_modal()

        with allure.step("Закрыть попап и дождаться его исчезновения"):
            order.close_success_modal_and_wait()  # закрываем попап

        main_window = driver.current_window_handle

        with allure.step("Логотип Самоката ведёт на главную страницу самоката"):
            main.click_scooter_logo()  # кликаем логотип для перехода на главную
            wait.until(EC.url_contains("qa-scooter.praktikum-services.ru"))  # ждём смены URL

            current_url = driver.current_url
            # Тут нужно убедиться, что страница заказа т.е /order больше не открыта
            assert "/order" not in current_url, (
                f"Ожидали главную страницу самоката, но URL всё ещё содержит /order: {current_url}"
            )

        with allure.step("Логотип Яндекса — новая вкладка, в URL есть dzen"):
            main.click_yandex_logo()  # кликаем логотип Яндекса и должна открыться новая вкладка
            wait.until(lambda d: len(d.window_handles) > 1)  # ждём

            new_handle = [h for h in driver.window_handles if h != main_window][0]
            driver.switch_to.window(new_handle)  # переключаемся на новую вкладку

            # Дзен открывается через редирект и мы даём больше времени
            WebDriverWait(driver, 30).until(lambda d: "dzen" in d.current_url.lower())
            assert "dzen" in driver.current_url.lower()  # убеждаемся, что попали на dzen.ru

            driver.close()  # закрываем вкладку Дзен
            driver.switch_to.window(main_window)  # возвращаемся на основную вкладку
