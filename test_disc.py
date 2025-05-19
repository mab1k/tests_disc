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

URL = "http://192.168.4.17/newdesign_old/disc/"
FILE_PATH = "/home/user/selenium/test.txt"
IMG_PATH = "/home/user/selenium/close.png"

expected_text = 'Text news'
expected_date = '30.12.2025'
expected_time = "12:00-18:00"

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.site_auto_button = (By.ID, "siteAuto")
        self.login_input = (By.ID, "floatingInput")
        self.password_input = (By.ID, "floatingPassword")
        self.auth_button = (By.ID, "authBtn")

    def login(self, username, password):
        self.driver.get(URL)
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.site_auto_button)).click()
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.login_input)).send_keys(username)
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.password_input)).send_keys(password)
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.auth_button)).click()

class DisciplinePage:
    def __init__(self, driver):
        self.driver = driver
        self.disc_button = (By.XPATH, "//button[contains(@class, 'accordion-button') and contains(@class, 'mb-0') and contains(., '2044 / 2045')]")
        self.modify_button = (By.CSS_SELECTOR, "button.btn.btn-info.disc_btn")

    def open_discipline(self):
        self.driver.get(URL)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.disc_button)).click()
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.modify_button)).click()
        time.sleep(3)

class NewsBlockPage:
    def __init__(self, driver):
        self.driver = driver
        self.news_block_button = (By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Новостной блок')]]")
        self.textarea = (By.CSS_SELECTOR, 'textarea.form-control[placeholder="Введите текст новости"]')
        self.add_news_button = (By.CSS_SELECTOR, "input.disc-btn-info[value='Добавить новость']")
        self.news_label = (By.XPATH, "//div[@id[starts-with(., 'elLabel')]]/p[contains(@class, 'h3') and contains(., 'Новости')]")
        self.news_date = (By.XPATH, "//p[contains(@class, 'm-0') and contains(text(), '-2025')]")
        self.news_text = (By.XPATH, "//div[@class='col-12']/p[contains(@class, 'text-wrap')]")
        self.delete_button = (By.CSS_SELECTOR, "button.btn.p-0.discEditCardControlBtn")

    def add_news(self, text):
        button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.news_block_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button)
        time.sleep(1.5)
        ActionChains(self.driver).move_to_element(button).click().perform()
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.textarea)).send_keys(text)
        
        add_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.add_news_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", add_button)
        time.sleep(1.5)
        ActionChains(self.driver).move_to_element(add_button).click().perform()

    def verify_news(self, expected_text):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.news_label))
        current_date_msk = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d-%m-%Y")
        news_date = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.news_date))
        assert news_date.text == current_date_msk
        news_text = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.news_text))
        assert news_text.text == expected_text

    def delete_news(self):
        delete_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.delete_button))
        ActionChains(self.driver).move_to_element(delete_button).perform()
        if delete_button.is_displayed() and delete_button.is_enabled():
            delete_button.click()
            
class AdBlockPage:
    def __init__(self, driver):
        self.driver = driver
        self.ad_block_button = (By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Объявление')]]")
        self.click_new_text = (By.CSS_SELECTOR, "#btnEditElName1682 path:nth-child(1)")
        self.input_text = (By.ID, "inputElName1682")
        self.button_add_ad = (By.ID, "text_block_button_1682")
        self.button_title = (By.ID, 'btnElName1682')
        self.verify_text = (By.ID, "elLabel1682")
        self.verify_text_text = (By.XPATH, '//div[@id="text_block_text_1682"]//td[p]/p')
        
    def add_button_ad(self):
        button_add = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.ad_block_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button_add)
        time.sleep(1.5)
        ActionChains(self.driver).move_to_element(button_add).click().perform()

    def add_ad(self, new_value):
        button_new_text = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.click_new_text))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button_new_text)
        time.sleep(1.5)
        ActionChains(self.driver).move_to_element(button_new_text).click().perform()
        
        input_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.input_text))
        input_element.clear()
        input_element.send_keys(new_value)
        
        button_title = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.button_title)).click()
    def set_content_in_tinymce_body(self, text):
        WebDriverWait(self.driver, 10).until(
            lambda d: d.execute_script("return typeof window.parent.tinymce !== 'undefined'")
        )

        content = f"<p>{text}</p>"

        self.driver.execute_script(f"""
            const editor = window.parent.tinymce.get('text_block_editor_1682');
        
            editor.setContent(`{content}`);
        
            editor.fire('change');
            editor.fire('input');
            editor.fire('keyup');
        """)
        
        button_add_ad = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.button_add_ad )).click()
    
    def verify_add(self, expected_text):
        element_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.verify_text)
        )
        extracted_text_title = element_title.text
        
        assert extracted_text_title == expected_text, "Text on block title ad, bad"
        
        element_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.verify_text_text)
        )
        extracted_text_text = element_text.text 
        
        assert extracted_text_text == expected_text, "Text on text block ad, bad"
        time.sleep(10)

class BlockTheManual:
    def __init__(self, driver):
        self.driver = driver
        self.add_block_button = (By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Блок с методичками')]]")
        self.add_new_block_title = (By.CSS_SELECTOR, "input.form-control[name='text'][placeholder='Введите название методички']")
        
    def add_button(self):
        button_add = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.add_block_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button_add)
        time.sleep(1.5)
        ActionChains(self.driver).move_to_element(button_add).click().perform()

    def add_new_block(self, expected_text):
        input_field_title = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.add_new_block_title)
        )
        input_field_title.send_keys(expected_text)
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", input_field_title)
        time.sleep(1.5)

        file_input = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input.form-control.d-none[name='manual'][onchange*='aman1687']")
            )
        )
        
        file_input.send_keys(FILE_PATH)
        
        file_input_img = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input.form-control.d-none[name='image'][onchange*='amanim1687']")
            )
        )
        
        file_input_img.send_keys(IMG_PATH)
        
        block = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@name='manual_block_id'][@value='1687']/ancestor::div[@class='row']")
            )
        )
        
        submit_button = block.find_element(
            By.CSS_SELECTOR, "input.btn-info.disc-btn-info[type='submit'][value='Добавить методичку']"
        )
        
        submit_button.click()
        time.sleep(10)
        
        input_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "inputManualTitle595"))
        )
        
        text_value = input_element.get_attribute("value")
        assert text_value == expected_text, "Text on block manual title, bad"
        time.sleep(10)
            
   
class CalendarBlockPage:
    def __init__(self, driver):
        self.driver = driver
        self.calendar_button = (By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Календарный план занятий')]]")
        self.text_input = (By.CSS_SELECTOR, "input.form-control[name='text']")
        self.date_input = (By.CSS_SELECTOR, "input.form-select[name='date']")
        self.start_input = (By.CSS_SELECTOR, "input.form-control[name='start']")
        self.end_input = (By.CSS_SELECTOR, "input.form-control[name='end']")
        self.add_lecture_button = (By.CSS_SELECTOR, 'input[value="Добавить лекцию"]')
        self.table_row = (By.CSS_SELECTOR, 'tr.green-background')
        self.theme_input = (By.XPATH, "//input[@type='text' and @size='72']")

    def add_lecture(self, text, date, start_time, end_time):
        
        button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.calendar_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button)
        time.sleep(1.5)
        ActionChains(self.driver).move_to_element(button).click().perform()
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.text_input)).send_keys(text)
        
        date_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.date_input))
        self.driver.execute_script("arguments[0].click();", date_element)
        date_element.send_keys(Keys.CONTROL + "a")
        date_element.send_keys(Keys.BACKSPACE)
        date_element.send_keys(date)
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.start_input)).send_keys(start_time)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.end_input)).send_keys(end_time)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_lecture_button)).click()

    def verify_lecture(self, expected_date, expected_time, expected_text):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        row = self.driver.find_element(*self.table_row)
        cells = row.find_elements(By.CSS_SELECTOR, 'td.table-cell')
        assert cells[0].text.strip() == expected_date
        assert cells[2].text.strip() == expected_time
        
        theme_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.theme_input))
        assert theme_input.get_attribute("value").strip() == expected_text

def test_registration(driver):
    login_page = LoginPage(driver)
    login_page.login("avz", "123")
    time.sleep(1)
    
@pytest.mark.skip
def test_news_block(driver):
    
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()
    
    news_page = NewsBlockPage(driver)
    news_page.add_news(expected_text)
    news_page.verify_news(expected_text)


@pytest.mark.skip
def test_calendar_block(driver):
    
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()
    
    calendar_page = CalendarBlockPage(driver)
    calendar_page.add_lecture(expected_text, expected_date, '12:00', '18:00')
    calendar_page.verify_lecture(expected_date, expected_time, expected_text)
    time.sleep(10)
    

@pytest.mark.skip
def test_ad(driver):
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()
    
    ad_block = AdBlockPage(driver)
    ad_block.add_ad(expected_text)
    ad_block.set_content_in_tinymce_body(expected_text)
    ad_block.verify_add(expected_text)

def test_block_the_manual(driver):
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()
    
    block_the_manual = BlockTheManual(driver)
    #block_the_manual.add_button()
    block_the_manual.add_new_block(expected_text)
