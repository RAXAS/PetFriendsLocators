import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter


def chrome_options(chrome_options):
   chrome_options.binary_location = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
   chrome_options.add_argument('--kiosk')
   return chrome_options

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:/Program Files/ChromeDriver/chromedriver.exe')
   # Переходим на страницу авторизации
   pytest.driver.get('https://petfriends.skillfactory.ru/login')
   yield
   pytest.driver.quit()

# Проверка страницы "мои питомцы"
def test_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('dima-pinsk@mail.ru')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('nanotehnik444')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Нажимаем на кнопку "мои питомцы"
   pytest.driver.find_element_by_xpath("//a[@class='nav-link']").click()
   # Проверяем, что мы оказались на странице "мои питомцы"
   assert pytest.driver.find_element_by_css_selector("html>body>div>div>div:nth-of-type(2)")

   # Для поиска css - $$("")
   # Получаем все фотографии питомцев на странице
   images = pytest.driver.find_elements_by_css_selector('div th > img')
   # Получаем всю информацию о питомцах на странице
   pets_info = pytest.driver.find_elements_by_css_selector('div td')
   # Сортируем информацию о питомцах и записываем в отдельные переменные
   names = pets_info[::5]
   breeds = pets_info[1::5]
   ages = pets_info[2::5]
   # Получаем информацию профиля и записываем в переменную
   amount = pytest.driver.find_elements_by_css_selector('html > body > div > div > div')
   # Создаём переменную для подсчёта колличества питомцев с фото
   pets_with_photo = 0
   # Создаём пустой список, в которые будем записывать имена питомцев
   list_names = []

   for i in range(len(names)):
      # Записываем колличество питомцев с фотографией
      if images[i].get_attribute('img') != '':
         pets_with_photo += 1
      # Проверяем, что у всех питомцев присутствует имя
      assert names[i].text != ''
      # Проверяем, что у всех питомцев присутствует порода
      assert breeds[i].text != ''
      # Проверяем, что у всех питомцев присутствует возраст
      assert ages[i].text != ''
      # Добавляем имена питомцев в список
      list_names.append(names[i].text)
   # Проверяем, что имя каждого животного уникально
   #for i in range(len(names)):
      #a = Counter(list_names)
      #print(a[i])
      #assert Counter(list_names)[i] == 1



   # Проверяем, что количество строк таблицы соответствует количеству питомцев в блоке статистики пользователя
   assert f"Питомцев: {len(names)}" in amount[0].text
   # Проверяем, что минимум у половины питомцев присутствует фотография
   assert pets_with_photo >= len(names) / 2
   # Проверяем, что у каждого питомца разное имя
   #assert



