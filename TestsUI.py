import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def chrome_options(chrome_options):
    chrome_options.set_headless(True)
    return chrome_options

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:/Program Files/ChromeDriver/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('https://petfriends.skillfactory.ru/login')
   yield
   pytest.driver.quit()


def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('dima-pinsk@mail.ru')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('nanotehnik444')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Нажимаем на кнопку "мои питомцы"
   pytest.driver.find_element_by_xpath("//a[@class='nav-link']").click()
   # Проверяем, что мы оказались на странице "мои питомцы"
   #assert pytest.driver.find_element_by_css_selector("html>body>div>div>div:nth-of-type(2)")

#def test_my_pets():

   images = pytest.driver.find_elements_by_css_selector('div#all_my_pets>table>tbody>tr:nth-of-type(1)>th>img')
   names = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')
   descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')

   for i in range(len(names)):
      assert images[i].get_attribute('src') != ''
      assert names[i].text != ''
      assert descriptions[i].text != ''
      assert ', ' in descriptions[i]
      parts = descriptions[i].text.split(", ")
      assert len(parts[0]) > 0
      assert len(parts[1]) > 0

