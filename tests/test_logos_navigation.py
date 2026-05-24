# Тесты навигации по логотипам в шапке страницы

import allure  

from pages.main_page import MainPage  


@allure.parent_suite("Тесты главной страницы")   # верхний уровень в разделе «Сюиты»
@allure.title("Логотипы в шапке")                # отображается вместо имени класса
@allure.feature("Главная страница")              # группировка в разделе «Категории»
@allure.story("Навигация по логотипам")         # подгруппа внутри «Категорий»


class TestHeaderLogosNavigation:

    #Проверяем поведение двух логотипов в шапке

    @allure.title("Логотип «Самокат» ведёт на главную, логотип Яндекса открывает Дзен")
    def test_scooter_and_yandex_logos(self, driver):  
        main = MainPage(driver)                        
        main_window = main.get_current_window_handle() 
                                                       

        with allure.step("Открыть главную и убрать cookies"):
            main.open()  # переходим на главную страницу
            main.accept_cookies_if_shown() # убираем баннер куки, если он появился

        with allure.step("Перейти к форме заказа через верхнюю кнопку «Заказать»"):
            main.click_order_top()  # переходим на страницу заказа — отсюда будем проверять потом редирект

        with allure.step("Логотип «Самокат» ведёт на главную страницу сервиса"):
            main.click_scooter_logo()          # кликаем по логотипу самоката
            main.wait_url_contains(main.get_site_host(), wait_timeout=20)  # ждём, пока URL изменится на главную
            current_url = main.get_current_url()
            base_url = main.get_base_url()
            assert current_url == base_url, (
                f"Ожидался URL {base_url}, но получен {current_url}"
            )

        with allure.step("Логотип Яндекса открывает новую вкладку с Дзеном"):
            main.click_yandex_logo()   # кликаем по логотипу Яндекса
            main.wait_until_window_count_greater_than(     # ждём появления второй вкладки
                1, wait_timeout=30
            )

            handles = main.get_window_handles()       # получаем список всех открытых вкладок
            new_handle = [h for h in handles if h != main_window][0]  # берём вкладку, которой не было
            main.switch_to_window(new_handle)        # переключаемся на новую вкладку
            main.wait_until_url_contains_case_insensitive(   # ждём загрузки Дзена 
                "dzen", wait_timeout=30
            )
            assert "dzen" in main.get_current_url().lower()   # проверка URL новой вкладки

            main.close_current_window()      # закрываем вкладку Дзена 
            main.switch_to_window(main_window)  # возвращаемся на исходную вкладку
