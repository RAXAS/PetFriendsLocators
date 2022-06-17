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
   pytest.driver.implicitly_wait(10)
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
   # Проверяем, что мы оказались на странице "все питомцы"
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located([By.CSS_SELECTOR, "html > body > div > div > div:nth-of-type(2)"]))
   # Нажимаем на кнопку "мои питомцы"
   pytest.driver.find_element_by_xpath("//a[@class='nav-link']").click()
   # Проверяем, что мы оказались на странице "мои питомцы"
   assert WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located([By.CSS_SELECTOR, "div#all_my_pets > table"]))
   # Получаем все фотографии питомцев на странице
   images = pytest.driver.find_elements_by_css_selector('div th > img')
   # Получаем всю информацию о питомцах на странице
   pets_info = pytest.driver.find_elements_by_css_selector('div td')
   # Сортируем информацию о питомцах и записываем в отдельные переменные
   names = pets_info[::4]
   breeds = pets_info[1::4]
   ages = pets_info[2::4]
   # Получаем информацию профиля и записываем в переменную
   amount = pytest.driver.find_elements_by_css_selector('html > body > div > div > div')
   # Создаём переменную для подсчёта колличества питомцев с фото
   pets_with_photo = 0
   # Создаём пустой список, в которые будем записывать имена всех питомцев
   list_names = []
   # Создаём пустой список, в который будем записывать всю информацию о каждом питомце
   all_pets = []

   for i in range(len(names)):
      # Проверяем, какое колличество питомцев с фотографией и записываем колличество в переменную
      if images[i].get_attribute('src') != '':
         pets_with_photo += 1
      # Проверяем, что у всех питомцев присутствует имя
      assert names[i].text != ''
      # Проверяем, что у всех питомцев присутствует порода
      assert breeds[i].text != ''
      # Проверяем, что у всех питомцев присутствует возраст
      assert ages[i].text != ''
      # Добавляем имена питомцев в список
      list_names.append(names[i].text)
      # Добавляем имена + породы + возраст каждого питомца в список
      all_pets.append(names[i].text + breeds[i].text + ages[i].text)
   # Проверяем, что нет повторяющихся питомцев
   assert len(Counter(all_pets)) == len(all_pets)
   # Проверяем, что имя каждого животного уникально
   assert len(Counter(list_names)) == len(list_names)
   # Проверяем, что количество строк таблицы соответствует количеству питомцев в блоке статистики пользователя
   assert f"Питомцев: {len(names)}" in amount[0].text
   # Проверяем, что минимум у половины питомцев присутствует фотография
   assert pets_with_photo >= len(names) / 2






