# Page Object страницы заказа: два шага формы и попап подтверждения

from selenium.webdriver import Keys  # тут клавиши клавиатуры: ESC, ENTER и тд
from selenium.webdriver.common.by import By  
from selenium.webdriver.remote.webelement import WebElement  
from selenium.webdriver.remote.webdriver import WebDriver  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.support.ui import WebDriverWait  


class OrderPage:

    #личные данные
    FIRST_NAME   = (By.XPATH, "//input[@placeholder='* Имя']")      # поле Имя
    LAST_NAME    = (By.XPATH, "//input[@placeholder='* Фамилия']")       # поле Фамилия
    ADDRESS      = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")     # поле адреса доставки
    METRO_INPUT  = (By.XPATH, "//input[@placeholder='* Станция метро']")      # поле поиск станции метро
    PHONE        = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")  # поле номера телефона
    BUTTON_NEXT  = (By.XPATH, "//button[text()='Далее']")       # переход дальше

    #параметры аренды
    DELIVERY_DATE = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")  # поле выбора даты; открывает календарь

    RENT_PERIOD_FIELD = (  # выбор Срока аренды
        By.XPATH,
        "//div[contains(@class,'Dropdown-placeholder') and contains(.,'Срок аренды')]",
    )

    BUTTON_ORDER = (  #кнопка «Заказать» на шаге 2, она  отличается от верхней и нижней кнопок с главной страницы
        By.XPATH,
        "//button[contains(@class,'Button_Middle') and text()='Заказать']",
    )

    #окно подтверждения 
    BUTTON_YES = (By.XPATH, "//button[text()='Да']")  # кнопка подтверждения в диалоге «Хотите оформить заказ?»

    MODAL_SUCCESS_HEADER = (  # заголовок попапа «Заказ оформлен» 
        By.XPATH,
        "//div[contains(@class,'Order_ModalHeader') and contains(.,'Заказ оформлен')]",
    )

    def __init__(self, driver: WebDriver, wait_timeout: int = 15):
        self.driver = driver                            
        self.wait = WebDriverWait(driver, wait_timeout) 

    @staticmethod
    def _scroll_into_view(element: WebElement) -> None:
        _ = element.location_once_scrolled_into_view  # прокрутка браузера к элементу 

    def fill_personal_data(self, first_name: str, last_name: str, address: str, phone: str):
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME)).send_keys(first_name)  # ждём появления формы и вводим имя
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)   # поля после первого ищем без ожидания тк форма уже есть
        self.driver.find_element(*self.ADDRESS).send_keys(address)        
        self.driver.find_element(*self.PHONE).send_keys(phone)           

    def select_metro(self, station_name: str):
        metro = self.wait.until(EC.element_to_be_clickable(self.METRO_INPUT))  # ждём пока поле метро станет кликабельным
        metro.click()                      
        metro.send_keys(station_name)       # вводим станцию

        option_xpath = f"//button[.//div[text()='{station_name}']]"  
        option = self.wait.until(EC.element_to_be_clickable((By.XPATH, option_xpath)))  # ждём 
        self._scroll_into_view(option)    # прокручиваем, чтобы станция поала в область видимости
        option.click()        # выбираем станцию 

        metro.send_keys(Keys.ESCAPE)        # на всякий случай закрываем список клавишей ESC

    def click_next(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_NEXT)).click()  # тут уже переходим к шагу 2

    def fill_rent_details(self, date_dd_mm_yyyy: str, period_label: str, color: str):
        date_el = self.wait.until(EC.visibility_of_element_located(self.DELIVERY_DATE))  # ждём поле даты 
        date_el.click()  # клик открывает календарь

        try:
            date_el.clear()  # пробуем очистить поле стандартным методом
        except Exception:
            date_el.send_keys(Keys.CONTROL, "a")  # если clear() не сработал — выделяем всё через Ctrl+A
            date_el.send_keys(Keys.BACKSPACE)      # а потом удаляем то что выделили

        date_el.send_keys(date_dd_mm_yyyy)  # вводим дату 
        date_el.send_keys(Keys.ESCAPE)    # закрываем календарь 

        self.wait.until(  # ждём пока календарь полностью закроется, так как некст клик может попасть в него
            EC.invisibility_of_element_located((By.CLASS_NAME, "react-datepicker__day-name")),
        )

        self.wait.until(EC.element_to_be_clickable(self.RENT_PERIOD_FIELD)).click()  # открываем «Срок аренды»

        period_xpath = (  
            f"//div[contains(@class,'Dropdown-menu')]//div[text()='{period_label}']"
            f" | //div[contains(@class,'Dropdown-option') and text()='{period_label}']"
        )
        period_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, period_xpath)))
        period_option.click()  # выбираем срок аренды 

        color_id = "black" if color.lower() in ("чёрный", "черный", "black") else "grey"  # определяем id чекбокса по цвету
        color_box = self.wait.until(EC.element_to_be_clickable((By.ID, color_id)))  # ждём 
        self._scroll_into_view(color_box)  # прокручиваем 
        color_box.click()    # выбираем нужный цвет

    def submit_order(self):
        self.wait.until(EC.element_to_be_clickable(self.BUTTON_ORDER)).click()  # нажимаем «Заказать» 

        try:
            yes = WebDriverWait(self.driver, 3).until(  # ждём кнопку «Да» не дольше 3 сек
                EC.element_to_be_clickable(self.BUTTON_YES),
            )
            yes.click()  # подтверждаем заказ 
        except Exception:
            pass  

    def wait_success_modal(self):
        # Ждём появления заголовка «Заказ оформлен» 
        self.wait.until(EC.visibility_of_element_located(self.MODAL_SUCCESS_HEADER))

    def close_success_modal_and_wait(self):
        # Закрываем попап и ждём его полного исчезновения перед кликом по логотипу
        BUTTON_VIEW_STATUS = (  # кнопка «Посмотреть статус» закрывает попап, но оставаясь на /order
            By.XPATH,
            "//button[contains(text(),'Посмотреть статус')]",
        )
        try:
            btn = self.wait.until(EC.element_to_be_clickable(BUTTON_VIEW_STATUS))  # ждём кнопку закрытия
            btn.click()  # закрываем
        except Exception:
            pass  

        self.wait.until(EC.invisibility_of_element_located(self.MODAL_SUCCESS_HEADER))  
