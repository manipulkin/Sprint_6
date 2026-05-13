# Page Object главной страницы стенда Самоката
# Локаторы вынесла в константы класса для удобства

from selenium.webdriver.common.action_chains import ActionChains  
from selenium.webdriver.common.by import By  
from selenium.webdriver.remote.webelement import WebElement  
from selenium.webdriver.remote.webdriver import WebDriver  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.support.ui import WebDriverWait  


class MainPage:

    URL = "https://qa-scooter.praktikum-services.ru/"  # базовый адрес стенда, ее будем использовать в тестах для проверки редиректа

    # Кнопка принятия куки — появляется при первом открытии сайта и перекрывает нижние элементы
    COOKIE_BUTTON = (
        By.XPATH,
        "//button[contains(@class,'CookieButton') or @id='rcc-confirm-button']",  
    )

    ORDER_BUTTON_TOP = (By.XPATH, "(//button[text()='Заказать'])[1]")       # кнопка «Заказать», которая находится в шапке страницы
    ORDER_BUTTON_BOTTOM = (By.XPATH, "(//button[text()='Заказать'])[last()]") # кнопка «Заказать», которая над футером

    LOGO_SCOOTER = (By.XPATH, "//a[contains(@class,'Header_LogoScooter')]")  # логотип Самоката в шапке
    LOGO_YANDEX = (By.XPATH, "//a[contains(@class,'Header_LogoYandex')]")    # логотип Яндекса в шапке

    def __init__(self, driver: WebDriver, wait_timeout: int = 15):
        self.driver = driver                            
        self.wait = WebDriverWait(driver, wait_timeout) # ожидаем 15 сек

    @staticmethod
    def _scroll_into_view(element: WebElement) -> None:
        _ = element.location_once_scrolled_into_view  # вызываем прокрутку браузера к нужному элементу

    def _click_after_scroll(self, element: WebElement) -> None:
        self._scroll_into_view(element)  # прокручиваем, чтобы элемент попал в область видимости
        ActionChains(self.driver).move_to_element(element).pause(0.15).click().perform()  

    def open(self):
        self.driver.get(self.URL)  # открываем главную страницу стенда

    def accept_cookies_if_shown(self):
        try:
            btn = WebDriverWait(self.driver, 3).until(  # ждём кнопку куки не дольше 3 с так как она не всегда появляется
                EC.element_to_be_clickable(self.COOKIE_BUTTON),
            )
            btn.click()  # закрываем баннер, чтобы он не перекрывал кнопки в нижней части 
        except Exception:
            pass  

    def click_order_top(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON_TOP))  # ждём появления кнопки в шапке
        el.click()  

    def click_order_bottom(self):
        el = self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON_BOTTOM))  # ждём, пока кнопка станет кликабельной
        # Тут при скроле элемент выравнивается под залипающую шапку которая его перекрывает, поэтому прокручиваемс к элементу, затем сдвигаем страницу вверх на 64px

        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)  #прокрутка к кнопке
        self.driver.execute_script("window.scrollBy(0, -64);")     #отступ от шапки
        el.click()

    def _faq_heading(self, index: int):
        return (By.ID, f"accordion__heading-{index}")  # заголовок (кнопка-стрелка) вопроса с нужным индексом

    def _faq_panel(self, index: int):
        return (By.XPATH, f"//div[@id='accordion__panel-{index}']")  # панель с текстом ответа, которая появляется после клика по заголовку

    def click_faq_question(self, index: int):
        heading = self.wait.until(EC.presence_of_element_located(self._faq_heading(index)))  
        self._click_after_scroll(heading)  # прокручиваем и кликаем

    def panel_text(self, index: int) -> str:
        panel = self.wait.until(EC.visibility_of_element_located(self._faq_panel(index)))  # ждём, пока текст ответа станет видимым
        return panel.text  # возвращаем текст 

    def click_scooter_logo(self):
        el = self.wait.until(EC.presence_of_element_located(self.LOGO_SCOOTER))  
        self._click_after_scroll(el)  # прокручиваем и клик

    def click_yandex_logo(self):
        el = self.wait.until(EC.presence_of_element_located(self.LOGO_YANDEX))  # ждём логотип Яндекса в шапке
        self._click_after_scroll(el)  # клик открывает Дзен в новой вкладке через редирект
