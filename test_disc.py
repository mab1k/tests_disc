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
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.news_block_button = (By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Новостной блок')]]")
        self.textarea = (By.CSS_SELECTOR, 'textarea.form-control[placeholder="Введите текст новости"]')
        self.add_news_button = (By.CSS_SELECTOR, "input.disc-btn-info[value='Добавить новость']")
        self.news_label = (By.XPATH, "//div[@id[starts-with(., 'elLabel')]]/p[contains(@class, 'h3') and contains(., 'Новости')]")
        self.news_date = (By.XPATH, "//p[contains(@class, 'm-0') and contains(text(), '-2025')]")
        self.news_text = (By.XPATH, "//div[@class='col-12']/p[contains(@class, 'text-wrap')]")
        self.delete_button = (By.CSS_SELECTOR, "button.btn.p-0.discEditCardControlBtn")

    def scroll_to_element(self, element, offset=-100):
        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(f"window.scrollTo(0, {location['y'] + offset});")
            time.sleep(0.3)
        except Exception as e:
            self._handle_exception("scroll_to_element", e)

    def click_with_js(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self._handle_exception("click_with_js", e)

    def _handle_exception(self, method_name, exception):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/error_{method_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"[ERROR] Ошибка в методе '{method_name}': {str(exception)}")
        print(traceback.format_exc())
        raise exception

    def add_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.news_block_button)
            )
            self.scroll_to_element(button)
            self.click_with_js(button)
        except Exception as e:
            self._handle_exception("add_button", e)

    def add_news(self, text):
        wait = WebDriverWait(self.driver, 10)
        try:
            textarea = wait.until(EC.visibility_of_element_located(self.textarea))
            self.scroll_to_element(textarea)
            textarea.send_keys(text)
            add_button = wait.until(EC.element_to_be_clickable(self.add_news_button))
            self.scroll_to_element(add_button)
            self.click_with_js(add_button)
        except Exception as e:
            self._handle_exception("add_news", e)

    def verify_news(self, expected_text):
        wait = WebDriverWait(self.driver, 10)
        try:
            current_date_msk = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%d-%m-%Y")
            news_date = wait.until(EC.visibility_of_element_located(self.news_date)).text
            assert news_date == current_date_msk
            news_text = wait.until(EC.visibility_of_element_located(self.news_text)).text
            assert news_text == expected_text
        except Exception as e:
            self._handle_exception("verify_news", e)

    def delete_news(self):
        try:
            delete_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.delete_button)
            )
            self.scroll_to_element(delete_button)
            if delete_button.is_displayed() and delete_button.is_enabled():
                self.click_with_js(delete_button)
        except Exception as e:
            self._handle_exception("delete_news", e)
            
class AdBlockPage:
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.ad_block_button = (By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Объявление')]]")
        self.click_new_text = (By.CSS_SELECTOR, "#btnEditElName1682 path:nth-child(1)")
        self.input_text = (By.ID, "inputElName1682")
        self.button_add_ad = (By.ID, "text_block_button_1682")
        self.button_title = (By.ID, 'btnElName1682')
        self.verify_text = (By.ID, "elLabel1682")
        self.verify_text_text = (By.XPATH, '//div[@id="text_block_text_1682"]//td[p]/p')

    def scroll_to_element(self, element, offset=-100):
        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(f"window.scrollTo(0, {location['y'] + offset});")
            time.sleep(0.3)
        except Exception as e:
            self._handle_exception("scroll_to_element", e)

    def click_with_js(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self._handle_exception("click_with_js", e)

    def _handle_exception(self, method_name, exception):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/error_{method_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"[ERROR] Ошибка в методе '{method_name}': {str(exception)}")
        print(traceback.format_exc())
        raise exception

    def add_button_ad(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.ad_block_button)
            )
            self.scroll_to_element(button)
            button.click()
        except Exception as e:
            self._handle_exception("add_button_ad", e)

    def add_ad(self, new_value):
        wait = WebDriverWait(self.driver, 10)
        try:
            button_new_text = wait.until(
                EC.element_to_be_clickable(self.click_new_text)
            )
            self.scroll_to_element(button_new_text)
            button_new_text.click()
            input_element = wait.until(
                EC.presence_of_element_located(self.input_text)
            )
            input_element.clear()
            input_element.send_keys(new_value)
            button_title = wait.until(
                EC.element_to_be_clickable(self.button_title)
            )
            self.scroll_to_element(button_title)
            self.click_with_js(button_title)
        except Exception as e:
            self._handle_exception("add_ad", e)

    def set_content_in_tinymce_body(self, text):
        try:
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
            button_add_ad = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.button_add_ad)
            )
            self.scroll_to_element(button_add_ad)
            self.click_with_js(button_add_ad)
        except Exception as e:
            self._handle_exception("set_content_in_tinymce_body", e)

    def verify_add(self, expected_text):
        wait = WebDriverWait(self.driver, 10)
        try:
            title = wait.until(
                EC.visibility_of_element_located(self.verify_text)
            ).text
            assert title == expected_text, "Заголовок объявления не совпадает"
            body = wait.until(
                EC.visibility_of_element_located(self.verify_text_text)
            ).text
            assert body == expected_text, "Текст объявления не совпадает"
        except Exception as e:
            self._handle_exception("verify_add", e)

class BlockTheManual:
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.add_block_button = (By.XPATH, "//button[contains(@class, 'disc-btn-info') and .//div[contains(text(), 'Блок с методичками')]]")
        self.add_new_block_title = (By.CSS_SELECTOR, "input.form-control[name='text'][placeholder='Введите название методички']")
        self.file_input = (By.CSS_SELECTOR, "input.form-control.d-none[name='manual'][onchange*='aman1687']")
        self.file_input_img = (By.CSS_SELECTOR, "input.form-control.d-none[name='image'][onchange*='amanim1687']")
        self.block = (By.XPATH, "//input[@name='manual_block_id'][@value='1687']/ancestor::div[@class='row']")
        self.submit_button = (By.XPATH, "(//input[@value='Добавить методичку'])[2]")
        self.input_element = (By.ID, "inputManualTitle595")

    def scroll_to_element(self, element, offset=-100):
        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(f"window.scrollTo(0, {location['y'] + offset});")
            time.sleep(0.3)
        except Exception as e:
            self._handle_exception("scroll_to_element", e)

    def click_with_js(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self._handle_exception("click_with_js", e)

    def _handle_exception(self, method_name, exception):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/error_{method_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"[ERROR] Ошибка в методе '{method_name}': {str(exception)}")
        print(traceback.format_exc())
        raise exception

    def add_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.add_block_button)
            )
            self.scroll_to_element(button)
            self.click_with_js(button)
        except Exception as e:
            self._handle_exception("add_button", e)

    def add_new_block(self, expected_text):
        wait = WebDriverWait(self.driver, 10)
        try:
            input_field_title = wait.until(
                EC.visibility_of_element_located(self.add_new_block_title)
            )
            self.scroll_to_element(input_field_title)
            input_field_title.send_keys(expected_text)

            file_input = wait.until(
                EC.visibility_of_element_located(self.file_input)
            )
            file_input.send_keys(FILE_PATH)

            file_input_img = wait.until(
                EC.visibility_of_element_located(self.file_input_img)
            )
            file_input_img.send_keys(IMG_PATH)

            submit_button = wait.until(
                EC.element_to_be_clickable(self.submit_button)
            )
            self.scroll_to_element(submit_button)
            self.click_with_js(submit_button)

            input_element = wait.until(
                EC.visibility_of_element_located(self.input_element)
            )
            assert input_element.get_attribute("value") == expected_text, "Название методички не совпадает"

        except Exception as e:
            self._handle_exception("add_new_block", e)
            
   
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
        
    def add_button():
        button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.calendar_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button)
        ActionChains(self.driver).move_to_element(button).click().perform()

    def add_lecture(self, text, date, start_time, end_time):
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.text_input)).send_keys(text)
        
        date_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.date_input))
        self.driver.execute_script("arguments[0].click();", date_element)
        date_element.send_keys(Keys.CONTROL + "a")
        date_element.send_keys(Keys.BACKSPACE)
        date_element.send_keys(date)
        
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.start_input)).send_keys(start_time)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.end_input)).send_keys(end_time)
        
        button_add = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_lecture_button))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", button_add)
        ActionChains(self.driver).move_to_element(button_add).click().perform()

    def verify_lecture(self, expected_date, expected_time, expected_text):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        row = self.driver.find_element(*self.table_row)
        cells = row.find_elements(By.CSS_SELECTOR, 'td.table-cell')
        assert cells[0].text.strip() == expected_date
        assert cells[2].text.strip() == expected_time
        
        theme_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.theme_input))
        assert theme_input.get_attribute("value").strip() == expected_text

class TableVisits:
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

        self.table_button = (By.XPATH, "//button/div[text()='Таблицу посещаемости']")
        self.input_date = (
            By.XPATH,
            "//input[@type='text' and @name='date' and contains(@class, 'form-control') "
            "and contains(@class, 'always-black') and contains(@class, 'bg-light') "
            "and contains(@class, 'always-black-sm')]"
        )
        self.input_name_student = (
            By.XPATH,
            "//input[@type='text' and @name='name' and contains(@class, 'form-control') "
            "and contains(@class, 'always-black') and contains(@class, 'bg-light') "
            "and contains(@class, 'always-black-sm')]"
        )
        self.button_date = (
            By.XPATH,
            "//div[contains(@class, 'col-sm-auto')]/input[@type='submit' and contains(@class, 'btn-info') and @value='Добавить']"
        )
        self.button_name = (
            By.XPATH,
            "//div[contains(@class, 'col-sm-1')]/input[@type='submit' and contains(@class, 'btn-info') and @value='Добавить']"
        )
        self.select_el = (By.XPATH, "//select[@class='form-select ' and @name='group']")
        self.button_students = (
            By.XPATH,
            "//div[contains(@class, 'col-sm-1')]/input[@type='submit' and contains(@class, 'btn-info') and @value='Добавить студентов в список']"
        )

    def scroll_to_element(self, element, offset=-100):
        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(f"window.scrollTo(0, {location['y'] + offset});")
            time.sleep(0.3)
        except Exception as e:
            self._handle_exception("scroll_to_element", e)

    def click_with_js(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self._handle_exception("click_with_js", e)

    def _handle_exception(self, method_name, exception):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/error_{method_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"[ERROR] Ошибка в методе '{method_name}': {str(exception)}")
        print(traceback.format_exc())
        raise exception

    def add_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.table_button)
            )
            self.scroll_to_element(button)
            self.click_with_js(button)
        except Exception as e:
            self._handle_exception("add_button", e)

    def add_date_students(self, input_date, input_name):
        try:
            wait = WebDriverWait(self.driver, 10)

            input_element_date = wait.until(
                EC.visibility_of_element_located(self.input_date)
            )
            input_element_date.clear()
            input_element_date.send_keys(input_date)

            button_date = wait.until(EC.element_to_be_clickable(self.button_date))
            self.scroll_to_element(button_date)
            self.click_with_js(button_date)

            input_element_name = wait.until(
                EC.visibility_of_element_located(self.input_name_student)
            )
            input_element_name.send_keys(input_name)

            button_stud = wait.until(EC.element_to_be_clickable(self.button_name))
            self.scroll_to_element(button_stud)
            self.click_with_js(button_stud)
            select_element = wait.until(
                EC.visibility_of_element_located(self.select_el)
            )
            self.scroll_to_element(select_element)
            select = Select(select_element)
            select.select_by_visible_text("КМБО-21-24")

            button_students = wait.until(
                EC.element_to_be_clickable(self.button_students)
            )
            self.scroll_to_element(button_students)
            self.click_with_js(button_students)

            time.sleep(5)
        except Exception as e:
            self._handle_exception("add_date_students", e)
    
    
class ListLectures:
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

        self.lectures_button = (By.XPATH, "//button/div[text()='Список литературы']")
        self.input_title = (By.XPATH, "(//input[@type='text' and @placeholder='Введите название'])[1]")
        self.button_add = (By.XPATH, "(//input[@type='button' and contains(@id, 'literature_add_item_button_')])[1]")
        self.actual_title = (By.XPATH, "(//tr[@valign='top']/td[contains(@id, 'literature_item_theme_')])[1]")
        self.actual_text = (By.XPATH, "(//div[contains(@id, 'literature_item_books_')])[1]")
        

    def scroll_to_element(self, element, offset=-100):
        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(f"window.scrollTo(0, {location['y'] + offset});")
            time.sleep(0.3)
        except Exception as e:
            self._handle_exception("scroll_to_element", e)

    def click_with_js(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self._handle_exception("click_with_js", e)

    def _handle_exception(self, method_name, exception):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/error_{method_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"[ERROR] Ошибка в методе '{method_name}': {str(exception)}")
        print(traceback.format_exc())
        raise exception
    
    def add_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.lectures_button)
            )
            self.scroll_to_element(button)
            self.click_with_js(button)
        except Exception as e:
            self._handle_exception("add_button", e)
            
    def add_lectures(self, input_text):
        wait = WebDriverWait(self.driver, 10)
        try:
            input_title = wait.until(
                EC.visibility_of_element_located(self.input_title)
            )
            self.scroll_to_element(input_title)
            input_title.send_keys(input_text)
            
            iframe_locator = (By.ID, "literature_editor_1590_ifr")
            wait.until(
                EC.frame_to_be_available_and_switch_to_it(iframe_locator)
            )

            editor_body = self.driver.find_element(By.TAG_NAME, "body")
            editor_body.clear()
            editor_body.send_keys(input_text)

            self.driver.switch_to.default_content()
            
            wait.until(
                EC.element_to_be_clickable(self.button_add)
            ).click()
            
            time.sleep(5)
            
        except Exception as e:
            self._handle_exception("add_lectures", e)
    def verify_add(self, expected_text):
        wait = WebDriverWait(self.driver, 10)
        
        try:
            actual_title = wait.until(
                EC.visibility_of_element_located(self.actual_title)
            ).text
            
            actual_text = wait.until(
                EC.visibility_of_element_located(self.actual_text)
            ).text
            
            assert actual_title == expected_text, "Bad text in title"
            assert actual_text == f"<p>{expected_text}</p>", "Bad text in text"
            
            time.sleep(5)
        except Exception as e:
            self._handle_exception("add_lectures", e)
        
class VideoBlock:
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

        self.video_button = (By.XPATH, "//button/div[text()='Блок с видео']")

    def scroll_to_element(self, element, offset=-100):
        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(f"window.scrollTo(0, {location['y'] + offset});")
            time.sleep(0.3)
        except Exception as e:
            self._handle_exception("scroll_to_element", e)

    def click_with_js(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self._handle_exception("click_with_js", e)

    def _handle_exception(self, method_name, exception):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/error_{method_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"[ERROR] Ошибка в методе '{method_name}': {str(exception)}")
        print(traceback.format_exc())
        raise exception
    
    def add_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.video_button)
            )
            self.scroll_to_element(button)
            self.click_with_js(button)
            time.sleep(5)
            
        except Exception as e:
            self._handle_exception("add_button", e)

class CourseWorkBlock:
    def __init__(self, driver):
        self.driver = driver
        self.screenshot_dir = "screenshots"
        os.makedirs(self.screenshot_dir, exist_ok=True)

        self.course_button = (By.XPATH, "//button/div[text()='Блок с курсовыми']")

    def scroll_to_element(self, element, offset=-100):
        try:
            location = element.location_once_scrolled_into_view
            self.driver.execute_script(f"window.scrollTo(0, {location['y'] + offset});")
            time.sleep(0.3)
        except Exception as e:
            self._handle_exception("scroll_to_element", e)

    def click_with_js(self, element):
        try:
            self.driver.execute_script("arguments[0].click();", element)
        except Exception as e:
            self._handle_exception("click_with_js", e)

    def _handle_exception(self, method_name, exception):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{self.screenshot_dir}/error_{method_name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        print(f"[ERROR] Ошибка в методе '{method_name}': {str(exception)}")
        print(traceback.format_exc())
        raise exception
    
    def add_button(self):
        try:
            button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.course_button)
            )
            self.scroll_to_element(button)
            self.click_with_js(button)
            time.sleep(5)
            
        except Exception as e:
            self._handle_exception("add_button", e)



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

#Debug
@pytest.mark.skip
def test_calendar_block(driver):
    
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()
    
    calendar_page = CalendarBlockPage(driver)
    calendar_page.add_lecture(expected_text, expected_date, '12:00', '18:00')
    calendar_page.verify_lecture(expected_date, expected_time, expected_text)
    
    

@pytest.mark.skip
def test_ad(driver):
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()
    
    ad_block = AdBlockPage(driver)
    ad_block.add_ad(expected_text)
    ad_block.set_content_in_tinymce_body(expected_text)
    ad_block.verify_add(expected_text)


#Debug
@pytest.mark.skip
def test_block_the_manual(driver):
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()
    
    block_the_manual = BlockTheManual(driver)
    #block_the_manual.add_button()
    block_the_manual.add_new_block(expected_text)


@pytest.mark.skip
def test_table_visits(driver):
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()

    table_visits = TableVisits(driver)
    #table_visits.add_button()
    table_visits.add_date_students(expected_date, expected_text)
    
@pytest.mark.skip
def test_list_lectures(driver):
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()

    list_lectures = ListLectures(driver)
    #list_lectures.add_button()
    list_lectures.add_lectures(expected_text)
    list_lectures.verify_add(expected_text)

@pytest.mark.skip
def test_video_block(driver):
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()

    video_block = VideoBlock(driver)
    video_block.add_button()

@pytest.mark.skip
def test_course_block(driver):
    discipline_page = DisciplinePage(driver)
    discipline_page.open_discipline()

    course_block = CourseWorkBlock(driver)
    course_block.add_button()
