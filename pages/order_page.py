# Page Object страницы оформления заказа
# тут шаг 1 (личные данные), шаг 2 (детали аренды), подтверждение и модальное окно

import allure                                  
from selenium.webdriver import Keys            
from selenium.webdriver.common.by import By    

from pages.base_page import BasePage           

#Page Object формы заказа самоката
class OrderPage(BasePage):

    # Локаторы шага 1 — личные данные  

    FIRST_NAME  = (By.XPATH, "//input[@placeholder='* Имя']")                              
    LAST_NAME   = (By.XPATH, "//input[@placeholder='* Фамилия']")                          
    ADDRESS     = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")      
    METRO_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")                   
    PHONE       = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    BUTTON_NEXT = (By.XPATH, "//button[text()='Далее']")     


    # Локаторы шага 2 — детали аренды

    DELIVERY_DATE = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")  # поле выбора даты

    # Дропдаун «Срок аренды» 
    RENT_PERIOD_FIELD = (
        By.XPATH,
        "//div[contains(@class,'Dropdown-placeholder') and contains(.,'Срок аренды')]",
    )

   
    # Локаторы подтверждения заказа

    # Кнопка «Заказать» на шаге 2
    BUTTON_ORDER = (
        By.XPATH,
        "//button[contains(@class,'Button_Middle') and text()='Заказать']",
    )

    BUTTON_YES = (By.XPATH, "//button[text()='Да']")  # кнопка подтверждения в диалоге «Вы уверены?»


    # Локаторы модального окна успеха

    # Заголовок попапа «Заказ оформлен» 
    MODAL_SUCCESS_HEADER = (
        By.XPATH,
        "//div[contains(@class,'Order_ModalHeader') and contains(.,'Заказ оформлен')]",
    )

    # Кнопка «Посмотреть статус» внутри попапа, которая закрывает модальное окно 
    BUTTON_VIEW_STATUS = (
        By.XPATH,
        "//button[contains(text(),'Посмотреть статус')]",
    )


    # Методы шага 1

    @allure.step("Заполнить персональные данные на шаге 1")
    def fill_personal_data(
        self,
        first_name: str,
        last_name: str,
        address: str,
        phone: str,
    ) -> None:
        
        #водим имя, фамилию, адрес и телефон.
        self.wait_visible(self.FIRST_NAME).send_keys(first_name)   # ждём поле и вводим имя
        self.wait_visible(self.LAST_NAME).send_keys(last_name)    # фамилия
        self.wait_visible(self.ADDRESS).send_keys(address)     # адрес доставки
        self.wait_visible(self.PHONE).send_keys(phone)    # номер телефона

    @allure.step("Выбрать станцию метро «{station_name}»")
    def select_metro(self, station_name: str) -> None:

        #кликаем по полю метро, вводим название, выбираем и закрываем
        metro = self.wait_clickable(self.METRO_INPUT)
        metro.click()               
        metro.send_keys(station_name)  # вводим название

        option_locator = (
            By.XPATH,
            f"//button[.//div[text()='{station_name}']]",
        )
        option = self.wait_clickable(option_locator)  # ждём появления станции в списке
        self.scroll_to_element_layout(option)     
        option.click()   # выбираем станцию

        metro.send_keys(Keys.ESCAPE)  # закрываем выпадающий список клавишей Escape

    @allure.step("Нажать «Далее» на шаге 1")
    def click_next(self) -> None:

        #переход к шагу 2 формы
        self.wait_clickable(self.BUTTON_NEXT).click()


    # Методы шага 2

    @allure.step("Заполнить дату доставки, срок аренды и цвет самоката")
    def fill_rent_details(self, date_dd_mm_yyyy: str, period_label: str, color: str) -> None:

        #вводим дату, выбираем срок аренды и отмечаем цвет
        date_el = self.wait_visible(self.DELIVERY_DATE)
        date_el.click()                        
        date_el.send_keys(Keys.CONTROL, "a")  # выделяем всё содержимое поля
        date_el.send_keys(Keys.BACKSPACE)  # стираем выделенное — поле теперь пустое
        date_el.send_keys(date_dd_mm_yyyy)  # вводим дату в формате ДД.ММ.ГГГГ
        date_el.send_keys(Keys.ESCAPE)  # закрываем календарь, если он открылся

        # Ждём пока календарь полностью закроется 
        self.wait_invisible(
            (By.CLASS_NAME, "react-datepicker__day-name"),  
        )

        #срок аренды 
        self.wait_clickable(self.RENT_PERIOD_FIELD).click()  # открываем список вариантов

        # Локатор опции 
        period_locator = (
            By.XPATH,
            (
                f"//div[contains(@class,'Dropdown-menu')]//div[text()='{period_label}']"
                f" | //div[contains(@class,'Dropdown-option') and text()='{period_label}']"
            ),
        )
        self.wait_clickable(period_locator).click()  # выбираем срок аренды

        #цвет самоката 
        color_id = "black" if color.lower() in ("чёрный", "черный", "black") else "grey"
        color_box = self.wait_clickable((By.ID, color_id))  # находим нужный чекбокс 
        self.scroll_to_element_layout(color_box)  
        color_box.click()   # отмечаем цвет

   
    # Методы подтверждения и проверки результата
  

    @allure.step("Отправить заказ и подтвердить в диалоге")
    def submit_order(self) -> None:

        self.wait_clickable(self.BUTTON_ORDER).click()    # кнопка «Заказать» на шаге 2
        self.wait_clickable(self.BUTTON_YES, wait_timeout=10).click()  # подтверждение в диалоге

    @allure.step("Дождаться модального окна «Заказ оформлен»")
    def wait_success_modal(self) -> None:

        #проверяем что после подтверждения появился попап с заголовком «Заказ оформлен»
        self.wait_visible(self.MODAL_SUCCESS_HEADER)  

    @allure.step("Закрыть окно успеха и дождаться его скрытия")
    def close_success_modal_and_wait(self) -> None:

        #кликаем «Посмотреть статус» и ждём, пока попап исчезнет
        self.wait_clickable(self.BUTTON_VIEW_STATUS).click()   # закрываем попап 
        self.wait_invisible(self.MODAL_SUCCESS_HEADER) # ждём исчезновения

