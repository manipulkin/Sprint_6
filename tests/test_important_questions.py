# Тесты блока «Вопросы о важном»

import allure
import pytest

from pages.main_page import MainPage


@allure.parent_suite("Тесты главной страницы")  # в разделе «Сюиты» — вместо имени test_important_questions
@allure.title("Тестирование раздела FAQ")              # вместо имени класса TestImportantQuestionsAccordion 
@allure.feature("Главная страница")            # группировка в разделе «Категории»
@allure.story("Вопросы о важном")              # подгруппа внутри 
class TestImportantQuestionsAccordion:

    # Список тест-кейсов для параметризации: (индекс вопроса и фрагмент ответа).
    FAQ_CASES = [
        (0, "Сутки — 400 рублей"),           # вопрос о стоимости
        (1, "один заказ — один самокат"),     # вопрос о нескольких самокатах
        (2, "Отсчёт времени аренды"),         # вопрос о расчёте времени
        (3, "Только начиная с завтрашнего дня"),  # вопрос о заказе на сегодня
        (4, "Пока что нет!"),                 # вопрос о продлении и досрочном возврате
        (5, "Этого хватает на восемь суток"), # вопрос о зарядке
        (6, "Да, пока самокат не привезли"),  # вопрос об отмене заказа
        (7, "Да, обязательно"),               # вопрос о доставке за МКАД
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
        "Один тестовый метод, но параметризация даёт восемь отдельных прогонов этих тестов — "
        "по одному на каждый вопрос из блока"
    )
    def test_each_faq_item_opens_matching_text(self, driver, question_index, expected_substring):
        main = MainPage(driver)  # создаём Page Object главной страницы

        with allure.step("Открыть главную страницу стенда"):
            main.open()  # переходим на URL стенда

        with allure.step("Убрать баннер куки, если он мешает"):
            main.accept_cookies_if_shown()  # баннер перекрывает нижние элементы и мы убираем его до начала теста

        with allure.step(f"Раскрыть вопрос с индексом {question_index}"):
            main.click_faq_question(question_index)  # кликаем по нужному заголовку

        with allure.step("Сравнить текст ответа с ожидаемым фрагментом"):
            text = main.panel_text(question_index)  # читаем текст из раскрывшейся панели
            assert expected_substring in text, (    # проверяем, что нужный фрагмент есть в ответе
                f"Не нашли «{expected_substring}» в ответе. Начало текста: {text[:220]!r}"  # выводим начало текста для диагностики
            )
