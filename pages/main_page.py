# Page Object главной страницы стенда «Яндекс.Самокат»
# Отвечает за: принятие куки, кнопки «Заказать», логотипы в шапке, блок FAQ

import allure                          
from selenium.webdriver.common.by import By  

from config.urls import BASE_URL, SITE_HOST
from pages.base_page import BasePage   

class MainPage(BasePage):

    # Локаторы

    COOKIE_BUTTON = (By.CSS_SELECTOR, "#rcc-confirm-button, button[class*='CookieButton']")

    ORDER_BUTTON_TOP = (
        By.XPATH,
        "//div[contains(@class,'Header_Header')]"
        "//button[contains(@class,'Button_Button') and normalize-space()='Заказать']",
    )

    ORDER_BUTTON_BOTTOM = (
        By.XPATH,
        "//div[contains(@class,'Home_FinishButton')]"
        "//button[contains(@class,'Button_Button') and normalize-space()='Заказать']",
    )

    LOGO_SCOOTER = (By.XPATH, "//a[contains(@class,'Header_LogoScooter')]")
    LOGO_YANDEX  = (By.XPATH, "//a[contains(@class,'Header_LogoYandex')]")

    @staticmethod
    def _faq_heading(index: int) -> tuple:
        return (By.ID, f"accordion__heading-{index}")

    @staticmethod
    def _faq_panel(index: int) -> tuple:
        return (By.ID, f"accordion__panel-{index}")

    @allure.step("Открыть главную страницу стенда")
    def open(self) -> None:
        self.open_url(BASE_URL)

    @allure.step("Принять cookies, если показан баннер")
    def accept_cookies_if_shown(self) -> None:
        self.click_if_clickable_within(self.COOKIE_BUTTON, timeout=3.0)

    @allure.step("Нажать «Заказать» в шапке страницы")
    def click_order_top(self) -> None:
        self.wait_clickable(self.ORDER_BUTTON_TOP).click()

    @allure.step("Нажать «Заказать» в блоке над футером")
    def click_order_bottom(self) -> None:
        element = self.wait_clickable(self.ORDER_BUTTON_BOTTOM)
        self.scroll_element_into_view(element)
        self.scroll_window_by(0, -64)
        element.click()

    @allure.step("Перейти к форме заказа (is_header={is_header})")
    def go_to_order(self, is_header: bool) -> None:
        if is_header:
            self.click_order_top()
        else:
            self.click_order_bottom()

    @allure.step("Раскрыть вопрос FAQ с индексом {index}")
    def click_faq_question(self, index: int) -> None:
        heading = self.wait_present(self._faq_heading(index))
        self.move_to_element_and_click(heading)

    @allure.step("Получить текст ответа FAQ с индексом {index}")
    def panel_text(self, index: int) -> str:
        panel = self.wait_visible(self._faq_panel(index))
        return panel.text

    @allure.step("Кликнуть по логотипу «Самокат» в шапке")
    def click_scooter_logo(self) -> None:
        element = self.wait_present(self.LOGO_SCOOTER)
        self.move_to_element_and_click(element)

    @allure.step("Кликнуть по логотипу Яндекса в шапке")
    def click_yandex_logo(self) -> None:
        element = self.wait_present(self.LOGO_YANDEX)
        self.move_to_element_and_click(element)

    @allure.step("Получить базовый URL стенда")
    def get_base_url(self) -> str:
        return BASE_URL

    @allure.step("Получить хост текущего стенда")
    def get_site_host(self) -> str:
        return SITE_HOST
    
