# Page Object главной страницы стенда «Яндекс.Самокат»
# Отвечает за: принятие куки, кнопки «Заказать», логотипы в шапке, блок FAQ

import allure                          
from selenium.webdriver.common.by import By  

from config.urls import BASE_URL, SITE_HOST
from pages.base_page import BasePage   

#Локаторы объявлены как атрибуты класса 
class MainPage(BasePage):

    # Локаторы


    # Кнопка принятия куки
    COOKIE_BUTTON = (By.CSS_SELECTOR, "#rcc-confirm-button, button[class*='CookieButton']")

    # Кнопка «Заказать» в шапке 
    ORDER_BUTTON_TOP = (
        By.XPATH,
        "//div[contains(@class,'Header_Header')]"
        "//button[contains(@class,'Button_Button') and normalize-space()='Заказать']",
    )

    # Кнопка «Заказать» перед футером
    ORDER_BUTTON_BOTTOM = (
        By.XPATH,
        "//div[contains(@class,'Home_FinishButton')]"
        "//button[contains(@class,'Button_Button') and normalize-space()='Заказать']",
    )

    # Логотипы в шапке 
    LOGO_SCOOTER = (By.XPATH, "//a[contains(@class,'Header_LogoScooter')]")
    LOGO_YANDEX  = (By.XPATH, "//a[contains(@class,'Header_LogoYandex')]")

 
    # Вспомогательные статические методы для динамических локаторов FAQ

    @staticmethod
    def _faq_heading(index: int) -> tuple:

        # возвращает локатор заголовка FAQ с заданным индексом
        return (By.ID, f"accordion__heading-{index}")  # id содержит порядковый номер вопроса

    @staticmethod
    def _faq_panel(index: int) -> tuple:
        
        #возвращает локатор панели-ответа FAQ с заданным индексом
        return (By.ID, f"accordion__panel-{index}")    # id содержит порядковый номер панели

   
    # Методы страницы
    # Над каждым добавила @allure.step, чтобы шаг отображался в отчёте
      

    @allure.step("Открыть главную страницу стенда")
    def open(self) -> None:
        
        self.open_url(BASE_URL)  # open_url определён в BasePage, он вызывает driver.get()

    @allure.step("Принять cookies, если показан баннер")
    def accept_cookies_if_shown(self) -> None:

        self.click_if_clickable_within(self.COOKIE_BUTTON, timeout=3.0) #кликаем по кнопке куки, если она появится в течение 3 секунд

    @allure.step("Нажать «Заказать» в шапке страницы")
    def click_order_top(self) -> None:

        self.wait_clickable(self.ORDER_BUTTON_TOP).click() #ждём кнопку в хедере и кликаем по ней

    @allure.step("Нажать «Заказать» в блоке над футером")
    def click_order_bottom(self) -> None:

        element = self.wait_clickable(self.ORDER_BUTTON_BOTTOM)
        self.scroll_element_into_view(element)  # прокручиваем, чтобы кнопка попала в область видимости
        self.scroll_window_by(0, -64)     # немного «отматываем» вверх так как хедер перекрывает 
        element.click()

    @allure.step("Раскрыть вопрос FAQ с индексом {index}")
    def click_faq_question(self, index: int) -> None:

        #прокручиваем к нужному заголовку FAQ и кликаем 
        heading = self.wait_present(self._faq_heading(index))  # ждём появления заголовка
        self.move_to_element_and_click(heading)   # скролл + наведение + клик

    @allure.step("Получить текст ответа FAQ с индексом {index}")
    def panel_text(self, index: int) -> str:

        panel = self.wait_visible(self._faq_panel(index))  # ждём, пока ответ раскроется и станет видим
        return panel.text      # возвращаем текст для сравнения в тесте

    @allure.step("Кликнуть по логотипу «Самокат» в шапке")
    def click_scooter_logo(self) -> None:

        #находим логотип самоката и кликаем
        element = self.wait_present(self.LOGO_SCOOTER)
        self.move_to_element_and_click(element)

    @allure.step("Кликнуть по логотипу Яндекса в шапке")
    def click_yandex_logo(self) -> None:
        
        #находим логотип Яндекса и кликаем, ожидаем открытие новой вкладки
        element = self.wait_present(self.LOGO_YANDEX)
        self.move_to_element_and_click(element)

    @allure.step("Получить базовый URL стенда")
    def get_base_url(self) -> str:
        #ПРАВКА локальный импорт убран  BASE_URL импортируется в шапке модуля
        return BASE_URL

    @allure.step("Получить хост текущего стенда")
    def get_site_host(self) -> str:
        #ПРАВКА локальный импорт убран, SITE_HOST импортируется в шапке модуля
        return SITE_HOST
    
