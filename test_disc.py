import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time
import os
import random
from datetime import datetime
import pytz

PROXY = '--proxy-server=http://192.168.4.219:3130'
URL = "http://192.168.4.17/newdesign_old/disc/"
FILE_PATH = "/home/user/selenium/close.png"

expected_text = 'Text news'
expected_date = '30.12.2025'
expected_time = "12:00-18:00"

def login(driver):
    try:
        driver.get(URL)  

        button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "siteAuto"))
        )
        button.click()

        login_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "floatingInput"))
        )
        login_input.send_keys("avz")

        password_input = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, "floatingPassword"))
        )
        password_input.send_keys("123")

        button_auth = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "authBtn"))
        )
        button_auth.click()
    except Exception:
        pytest.fail("Авторизация прошла не успешно")
        

def test_registration(driver):
    login(driver)
    
    time.sleep(1)
@pytest.mark.skip
def test_news_block(driver):
    try:
        driver.get(URL) 
        button_disc = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'accordion-button') and contains(@class, 'mb-0') and contains(., '2044 / 2045')]"))
        )
        button_disc.click()
        
        button_modify = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-info.disc_btn"))
        )
        button_modify.click()
        
        time.sleep(3)
        
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Новостной блок')]]"))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button)


        time.sleep(1.5)

        ActionChains(driver).move_to_element(button).click().perform()
        
        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea.form-control[placeholder="Введите текст новости"]'))
        )
        
        textarea.send_keys(expected_text)
        
        button_add_news = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.disc-btn-info[value='Добавить новость']"))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button_add_news)

        time.sleep(1.5)

        ActionChains(driver).move_to_element(button_add_news).click().perform()
        
        
        news_label = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id[starts-with(., 'elLabel')]]/p[contains(@class, 'h3') and contains(., 'Новости')]"))
        )
        print("Заголовок 'Новости' найден")
        msk_timezone = pytz.timezone('Europe/Moscow')
        current_date_msk = datetime.now(msk_timezone).strftime("%d-%m-%Y")
        
        news_date = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'm-0') and contains(text(), '-2025')]"))
        )

        if news_date.text == current_date_msk:
            print(f"Дата новости совпадает с текущей: {current_date_msk}")
        else:
            raise AssertionError(f"Дата новости {news_date.text} не совпадает с текущей {current_date_msk}")

        news_text = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@class='col-12']/p[contains(@class, 'text-wrap')]"))
        )
        
        
        if news_text.text == expected_text:
            print(f"Текст новости совпадает: '{expected_text}'")
        else:
            raise AssertionError(f"Текст новости '{news_text.text}' не совпадает с ожидаемым '{expected_text}'")
  
            
        delete_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.p-0.discEditCardControlBtn"))
        )
        ActionChains(driver).move_to_element(delete_button).perform()

        if delete_button.is_displayed() and delete_button.is_enabled():
            delete_button.click()
            print("Кнопка 'Удалить' нажата")
        else:
            print("Кнопка недоступна для клика")
        
        #confirm_modal = WebDriverWait(driver, 10).until(
        #    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'modal') and contains(.//*, 'Вы точно хотите удалить этот блок?')]"))
      #  )
        
       #
       # confirm_button = WebDriverWait(confirm_modal, 10).until(
       #     EC.element_to_be_clickable((By.XPATH, ".//button[contains(., 'Да') or contains(., 'OK')]"))
       # )
       # confirm_button.click()
        
       # WebDriverWait(driver, 10).until(
       #     EC.invisibility_of_element_located((By.XPATH, "//div[contains(@class, 'modal')]"))
       # )
      #  
       # print("Удаление успешно подтверждено")
        
       # time.sleep(5)
       # print("Кнопка 'Удалить' нажата")
    except Exception:
        pytest.fail("Авторизация прошла не успешно")

def test_calendar_block(driver):
    try:
        driver.get(URL) 
        button_disc = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'accordion-button') and contains(@class, 'mb-0') and contains(., '2044 / 2045')]"))
        )
        button_disc.click()
        
        button_modify = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-info.disc_btn"))
        )
        button_modify.click()
        
        time.sleep(3)
        
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Календарный план занятий')]]"))
        )
        
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button)

        time.sleep(1.5)

        ActionChains(driver).move_to_element(button).click().perform()
        
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control[name='text']"))
        )
        input_element.send_keys(expected_text)
        
        date_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-select[name='date']"))
        )
        
        driver.execute_script("arguments[0].click();", date_input)
        date_input.send_keys(Keys.CONTROL + "a")  # Выделяем весь текст (для Windows)
        date_input.send_keys(Keys.BACKSPACE)
    
        date_input.send_keys(expected_date) 
        
        start_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control[name='start']"))
        )

        start_input.send_keys('12:00')
        
        end_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.form-control[name='end']"))
        )
    
        end_input.send_keys('18:00')
        
        
        
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][name='image']"))
        )
    
        file_path = os.path.abspath(FILE_PATH)
    
        file_input.send_keys(file_path)
        
        add_lecture_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.btn.btn-info[name='Добавить лекцию']"))
        )
    
        add_lecture_button.click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )

        date_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Дата')]/following-sibling::td[1]")
        time_element = driver.find_element(By.XPATH, "//td[contains(text(), 'Время')]")

        actual_date = date_element.text.strip()
        actual_time = time_element.text.strip()

        if actual_date == expected_date and actual_time == expected_time:
            print("Значения даты и времени совпадают.")
        else:
            print(f"Значения не совпадают. Ожидалось: {expected_date} и {expected_time}, получено: {actual_date} и {actual_time}.")
            
        input_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='text' and @size='72']"))
            )   

        actual_theme_value = input_element.get_attribute("value").strip()

        if actual_theme_value == expected_text:
            print("Значение темы совпадает.")
        else:
            print(f"Значение не совпадает. Ожидалось: '{expected_theme_value}', получено: '{actual_theme_value}'.")
        time.sleep(10)
    except Exception:
        pytest.fail("Авторизация прошла не успешно")
