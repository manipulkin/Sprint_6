# Тесты блока «Вопросы о важном»

import allure   
import pytest   

from pages.main_page import MainPage  # Page Object главной страницы


# Декораторы 
@allure.parent_suite("Тесты главной страницы")  # верхний уровень в разделе «Сюиты»
@allure.title("Тестирование раздела FAQ")    # отображается вместо имени класса
@allure.feature("Главная страница")      # группировка в разделе «Категории»
@allure.story("Вопросы о важном")      # подгруппа внутри «Категорий»

#Тесты FAQ
class TestImportantQuestionsAccordion:

    # Список тест-кейсов для параметризации: (индекс вопроса и фрагмент ответа).
    FAQ_CASES = [
        (0, "Сутки — 400 рублей"),               # стоимость аренды
        (1, "один заказ — один самокат"),         # ограничение: один самокат на заказ
        (2, "Отсчёт времени аренды"),           # как считается время аренды
        (3, "Только начиная с завтрашнего дня"),  # нельзя заказать на сегодня
        (4, "Пока что нет!"),                     # продление и досрочный возврат
        (5, "Этого хватает на восемь суток"),     # ресурс зарядки батареи
        (6, "Да, пока самокат не привезли"),      # условия отмены заказа
        (7, "Да, обязательно"),     # доставка за МКАД
    ]

    @pytest.mark.parametrize(
        "question_index, expected_substring",  
        FAQ_CASES,                             
        ids=[                                  
            "faq_price",          
            "faq_many_scooters",  
            "faq_rent_time",      
            "faq_today",          
            "faq_extend",         
            "faq_charger",       
            "faq_cancel",        
            "faq_mkad",           
        ],
    )

    @allure.title("FAQ: по клику открывается ответ с нужным текстом")
    @allure.description(
        "Параметризация даёт восемь отдельных прогонов — "
        "по одному на каждый вопрос из блока «Вопросы о важном»"
    )
    def test_each_faq_item_opens_matching_text(
        self,
        driver,                    
        question_index,            
        expected_substring,       
    ):
        main = MainPage(driver)  

        with allure.step("Открыть главную страницу стенда"):
            main.open()                      # переходим на URL стенда (из config/urls.py)

        with allure.step("Убрать баннер куки, если он мешает"):
            main.accept_cookies_if_shown()   # убираем до начала баннер так как он перекрывает нижние элементы 

        with allure.step(f"Раскрыть вопрос с индексом {question_index}"):
            main.click_faq_question(question_index)  # прокручиваем и кликаем по нужному заголовку

        with allure.step("Сравнить текст ответа с ожидаемым фрагментом"):
            text = main.panel_text(question_index)  # ждём видимости панели и читаем её текст
            assert expected_substring in text, (    # проверяем
                f"Не нашли «{expected_substring}» в ответе. "
                f"Начало текста: {text[:220]!r}"   # выводим первые 220 символов для диагностики
            )

