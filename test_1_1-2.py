import os
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from pathlib import Path

home_directory = str(Path.home())
download_folder_name = str(uuid.uuid4())
download_folder_path = os.path.join(home_directory, download_folder_name)


@pytest.fixture
def browser():
    print("\nstart browser for test..")
    chrome_options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_folder_path}
    chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    yield browser
    # При завершении теста
    print("\nquit browser..")
    browser.quit()


class TestGosUslugi():
    def test_one(self, browser):
        link = "https://www.gosuslugi.ru"
        browser.get(link)
        browser.implicitly_wait(20)

        time.sleep(5)
        browser.execute_script("document.getElementById('_epgu_el1').click()")
        input1 = browser.find_element_by_id("_epgu_el1")  # Находим поисковую строку
        input1.send_keys("загран")

        browser.find_element_by_xpath("//*[text()='загранпаспорт нового поколения 18 лет']").click()

        button = browser.find_element_by_xpath("//*[text()=' гражданином Российской Федерации достигшим ']")
        ActionChains(browser).move_to_element(button).perform()  # Скроллим до  нужного элемента
        button.click()

        button2 = browser.find_element_by_css_selector(".btn-sec.larr_svg")  # Кнопка вернуться
        button2.click()
        button3 = browser.find_element_by_css_selector(".btn-sec.small.larr_svg")  # Кнопка вернуться
        button3.click()
        button4 = browser.find_element_by_css_selector(".btn-sec.small.larr")  # Кнопка вернуться в каталог
        button4.click()

        massage = browser.find_element_by_css_selector(".h1.offset-top-none")
        assert massage.text in "Каталог госуслуг", "Значения разные"  # Проверка отображения "Каталог госуслуг"

    def test_second(self, browser):

        link = "https://www.gosuslugi.ru/situation/obtaining_drivers_license_first_time"
        browser.get(link)
        browser.implicitly_wait(20)

        button = browser.find_element_by_css_selector('[href="http://www.gibdd.ru/"]')
        ActionChains(browser).move_to_element(button).perform()
        button.click()  # Переходим на сайт Госавтоинспекции
        #time.sleep(5) добавляются при долгой прогрузке страниц, связанной с интернетсоединением, а также с версией Google Chrome

        new_window = browser.window_handles[1]
        browser.switch_to.window(new_window)  # Переходим в новое окно
        button1 = browser.find_element_by_css_selector('[href="/banners/redirect?bid=4"]')
        ActionChains(browser).move_to_element(button1).perform()
        button1.click()  # Переходим на сайт МВД России
        #time.sleep(5)

        new_window = browser.window_handles[2]
        browser.switch_to.window(new_window)  # Переходим в следующее окно
        input1 = browser.find_element_by_css_selector('#menu-1 > li:nth-child(1)')
        input1.click()
        input2 = browser.find_element_by_css_selector('[href="/mvd/documents"]')
        input2.click()
        #time.sleep(5)

        button1 = browser.find_element_by_css_selector('[ href="/mvd/documents/other-docs"]')
        ActionChains(browser).move_to_element(button1).perform()
        button1.click()  # Переходим в документы
        input3 = browser.find_element_by_css_selector(
            ".file_table > tbody > tr:nth-child(1) > td:nth-child(2) > a")
        input3.click()
        # Ждём, когда директория для загруженных файлов будет создана
        time.sleep(2)
        still_downloading = True
        while still_downloading:
            still_downloading = False
            for i in os.listdir(download_folder_path):
                if ".crdownload" in i:
                    time.sleep(0.5)
                    still_downloading = True
        # Убеждааемся, что в папке находится скачанный файл
        assert next(os.walk(download_folder_path))[2], "Файл не был скачан"
        # Удаляем скачанный файл и папку
        for f in next(os.walk(download_folder_path))[2]:
            os.remove(os.path.join(download_folder_path, f))
        os.rmdir(download_folder_path)

