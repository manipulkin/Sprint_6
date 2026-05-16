# Базовый Page Object, в котором: прямой контакт с WebDriver, открытие URL, ожидания, клики, скролл, работа с вкладками
# Дочерние страницы (MainPage, OrderPage) наследуются от этого класса и пользуются его методами
 
from __future__ import annotations  
 
from typing import List, Tuple       
 
import allure                                             
from selenium.webdriver.common.by import By             
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.remote.webdriver import WebDriver         
from selenium.webdriver.remote.webelement import WebElement       
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait           
from selenium.common.exceptions import TimeoutException  
 
 
Locator = Tuple[By, str]
 
#Базовый класс для всех Page Object проекта: инкапсулируем driver и WebDriverWait
class BasePage:
    
    @allure.step("Инициализация BasePage")
    def __init__(self, driver: WebDriver, wait_timeout: int = 15) -> None:
        self._driver = driver                              # храним драйвер как атрибут
        self._wait = WebDriverWait(driver, wait_timeout)  #  ожидание 15 сек для всех методов
 
   
    #  Навигация     
 
    @allure.step("Открыть URL «{url}»")  
    def open_url(self, url: str) -> None:
        self._driver.get(url)  # место в проекте, где вызывается driver.get()
 
    
    #  Поиск элементов     
 
    @allure.step("Найти все элементы по локатору {locator}")
    def find_elements(self, locator: Locator) -> List[WebElement]: 
        
        return self._driver.find_elements(*locator)  #Возвращаем список всех найденных элементов (пустой список, если ничего нет)
 
    
    #  Клики: используется для необязательных элементов (например, баннер куки), чтобы не падать, если баннера нет
    
    @allure.step("Кликнуть по элементу, если он станет кликабельным в течение {timeout} с")
    def click_if_clickable_within(self, locator: Locator, timeout: float = 3.0) -> bool:
        #ПРАВКА локальный импорт TimeoutException убрала — он теперь в шапке файла
        try:
            element = WebDriverWait(self._driver, timeout).until(
                lambda d: next((el for el in self.find_elements(locator) 
                                if el.is_displayed() and el.is_enabled()), None)
            )
            if element:
                element.click()
                return True
            return False
        except TimeoutException:
            return False
 
    @allure.step("Дождаться кликабельности элемента {locator}")
    def wait_clickable(self, locator: Locator, wait_timeout: int | None = None) -> WebElement:  
        
        #ждём, пока элемент станет кликабельным, и возвращаем его
 
        wait = self._wait if wait_timeout is None else WebDriverWait(self._driver, wait_timeout)
        return wait.until(EC.element_to_be_clickable(locator))  # бросает TimeoutException при провале
 
    @allure.step("Дождаться видимости элемента {locator}")
    def wait_visible(self, locator: Locator, wait_timeout: int | None = None) -> WebElement:
 
        # Ждём, пока элемент станет видимым 
        wait = self._wait if wait_timeout is None else WebDriverWait(self._driver, wait_timeout)
        return wait.until(EC.visibility_of_element_located(locator))
 
    @allure.step("Дождаться присутствия элемента {locator}")
    def wait_present(self, locator: Locator, wait_timeout: int | None = None) -> WebElement:
 
        #ждём присутствия элемента 
        wait = self._wait if wait_timeout is None else WebDriverWait(self._driver, wait_timeout)
        return wait.until(EC.presence_of_element_located(locator))
 
    @allure.step("Дождаться скрытия элемента {locator}")
    def wait_invisible(self, locator: Locator, wait_timeout: int | None = None) -> None:
 
        # ждём, пока элемент исчезнет 
        wait = self._wait if wait_timeout is None else WebDriverWait(self._driver, wait_timeout)
        wait.until(EC.invisibility_of_element_located(locator))
 
    
    #  Ожидания URL и вкладок  
    
 
    @allure.step("Дождаться, пока URL будет содержать «{fragment}»")
    def wait_url_contains(self, fragment: str, wait_timeout: int = 20) -> None:
 
        #Ждём, пока текущий URL не будет содержать нужный фрагмент
        WebDriverWait(self._driver, wait_timeout).until(EC.url_contains(fragment))
 
    @allure.step("Дождаться числа вкладок больше {count}")
    def wait_until_window_count_greater_than(self, count: int, wait_timeout: int = 30) -> None:

        #Ждём пока не откроется дополнительная вкладка (которая после click по внешней ссылке)
        WebDriverWait(self._driver, wait_timeout).until(
            lambda d: len(d.window_handles) > count  # проверяем  кол-во открытых окон
        )
 
    @allure.step("Дождаться URL с подстрокой «{substring}» (без учёта регистра)")
    def wait_until_url_contains_case_insensitive(self, substring: str, wait_timeout: int = 30) -> None:
 
        #Ждём совпадения подстроки в URL (нужно для dzen.ru / Dzen.ru)
        needle = substring.lower()  # приводим искомую строку к нижнему регистру
 
        def _predicate(driver: WebDriver) -> bool:
            return needle in driver.current_url.lower()  # сравниваем оба 
 
        WebDriverWait(self._driver, wait_timeout).until(_predicate)
 
    
    #  Работа с вкладками  
    
 
    @allure.step("Получить текущий URL")
    def get_current_url(self) -> str:
        return self._driver.current_url  # прямое обращение к driver 
 
    @allure.step("Получить дескриптор текущей вкладки")
    def get_current_window_handle(self) -> str:
        return self._driver.current_window_handle  # уникальный идентификатор текущей вкладки
 
    @allure.step("Получить список дескрипторов вкладок")
    def get_window_handles(self) -> List[str]:
        return list(self._driver.window_handles)  # список всех открытых вкладок в браузере
 
    @allure.step("Переключиться на вкладку {handle}")
    def switch_to_window(self, handle: str) -> None:
        self._driver.switch_to.window(handle)  # переключаемся на вкладку 
 
    @allure.step("Закрыть текущую вкладку")
    def close_current_window(self) -> None:
        self._driver.close()  # закрывает только текущую вкладку
 
    
    #  Скролл и взаимодействие с элементами 
   
 
    @allure.step("Прокрутить элемент в зону видимости (scrollIntoView)")
    def scroll_element_into_view(self, element: WebElement) -> None:

        #Прокручивает страницу чтобы элемент оказался в видимой области        
        self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
        
 
    @allure.step("Прокрутить страницу к элементу (layout)")
    def scroll_to_element_layout(self, element: WebElement) -> None:

        #скроллим через обращение к location_once_scrolled_into_view        
        _ = element.location_once_scrolled_into_view  
 
    @allure.step("Прокрутить окно на ({delta_x}, {delta_y})")
    def scroll_window_by(self, delta_x: int, delta_y: int) -> None:

        #прокрутка окна на delta_x пикселей вправо и delta_y — вниз    
        self._driver.execute_script(
            "window.scrollBy(arguments[0], arguments[1]);", delta_x, delta_y
        )
 
    @allure.step("Прокрутить к элементу и выполнить клик мышью")
    def move_to_element_and_click(self, element: WebElement) -> None:
        #перемещаем курсор к элементу и кликаем по нему через ActionChains
        
        _ = element.location_once_scrolled_into_view  # сначала прокручиваем к элементу
        (
            ActionChains(self._driver)
            .move_to_element(element)  # наводим курсор
            .pause(0.15)  
            .click()       # кликаем
            .perform()        # выполняем всю цепочку
        )
