# Позитивный сценарий оформления заказа — до появления окна «Заказ оформлен»

import allure  
import pytest   

from pages.main_page import MainPage   
from pages.order_page import OrderPage 


@allure.parent_suite("Тесты оформления заказа")  # верхний уровень в разделе «Сюиты»
@allure.title("Позитивный сценарий заказа")   # отображается вместо имени класса
@allure.feature("Оформление заказа")    # группировка в разделе «Категории»
@allure.story("Позитивный сценарий")   # подгруппа внутри «Категорий»

#Проверка оформлления заказа
class TestOrderHappyPath:

    # Первый набор данных: клиент Акакий, верхняя кнопка «Заказать»
    CUSTOMER_AKAKIY = {
        "first_name": "Акакий",
        "last_name":  "Огурцов",
        "phone":      "+79998884545",
        "metro":      "Черкизовская",
        "address":    "г. Москва, ул. Тестовая, д. 1",
        "date":       "01.12.2026",    # формат ДД.ММ.ГГГГ
        "period":     "сутки",         # метка из дропдауна «Срок аренды»
        "color":      "чёрный",        # название цвета на русском
    }

    # Второй набор данных: клиентка Агафья, нижняя кнопка «Заказать»
    CUSTOMER_AGAFYA = {
        "first_name": "Агафья",
        "last_name":  "Ручковна",
        "phone":      "+79031234567",
        "metro":      "Сокольники",
        "address":    "г. Москва, ул. Примерная, д. 2",
        "date":       "05.12.2026",
        "period":     "двое суток",
        "color":      "серый",
    }

    @pytest.mark.parametrize(
        "use_bottom_entry, customer",   
        [
            pytest.param(
                False,    # False = верхняя кнопка
                CUSTOMER_AKAKIY,  # данные первого клиента
                id="header_button_akkakiy",  
            ),
            pytest.param(
                True,           # True  = нижняя кнопка
                CUSTOMER_AGAFYA,   # данные второго клиента
                id="footer_button_agafya",   
            ),
        ],
    )
    @allure.title("Оформление заказа до модального окна «Заказ оформлен»")
    def test_positive_order_flow_success_modal(
        self,
        driver,            
        use_bottom_entry,  # True — нижняя кнопка, False — верхняя
        customer,          # данные клиента
    ):
        #подставляем параметры в Allure-отчёт 
        entry_label = "Нижняя «Заказать»" if use_bottom_entry else "Верхняя «Заказать»"
        allure.dynamic.parameter("Точка входа", entry_label)
        allure.dynamic.parameter("Клиент", f"{customer['first_name']} {customer['last_name']}")

        main  = MainPage(driver)   
        order = OrderPage(driver)  

        with allure.step("Главная страница"):
            main.open()            # открываем стенд
            main.accept_cookies_if_shown() # убираем баннер куки, если он есть

        with allure.step("Перейти к форме заказа"):
            if use_bottom_entry:
                main.click_order_bottom()  # нижняя кнопка «Заказать» (перед футером)
            else:
                main.click_order_top() # верхняя кнопка «Заказать» (в шапке)

        with allure.step("Шаг 1 формы — личные данные и метро"):
            order.fill_personal_data(      # заполняем имя, фамилию, адрес, телефон
                customer["first_name"],
                customer["last_name"],
                customer["address"],
                customer["phone"],
            )
            order.select_metro(customer["metro"])  # отдельно выбираем метро 

        with allure.step("Шаг 2 формы — дата, срок, цвет"):
            order.click_next()         # переходим к шагу 2
            order.fill_rent_details(     
                customer["date"],
                customer["period"],
                customer["color"],
            )

        with allure.step("Отправить заказ"):
            order.submit_order()           # нажимаем «Заказать» и подтверждаем 

        with allure.step("Проверить попап «Заказ оформлен»"):
            order.wait_success_modal()     

        with allure.step("Закрыть попап и дождаться его исчезновения"):
            order.close_success_modal_and_wait()  # кликаем «Посмотреть статус», ждём скрытия попапа
