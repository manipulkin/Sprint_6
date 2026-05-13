# Общие фикстуры для всех тестов проекта Sprint_6.

import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # настраиваем запуск Firefox
from selenium.webdriver.firefox.service import Service  
from webdriver_manager.firefox import GeckoDriverManager  


#путь к geckodriver определяется ОДИН РАЗ на весь запуск, без этого проьлема ConnectionError на втором-третьем тесте из за плохого соединения
@pytest.fixture(scope="session")
def geckodriver_path():
    
    return GeckoDriverManager().install()


#каждый тест получает свой чистый браузер
@pytest.fixture
def driver(geckodriver_path):  # geckodriver_path пробрасывается из session-фикстуры выше
    opts = Options()  

    service = Service(geckodriver_path)           
    browser = webdriver.Firefox(service=service, options=opts) 

    browser.maximize_window()  #разворачиваем на весь экран

    yield browser  # отдаём браузер в тест

    browser.quit()  # закрываем браузер 
