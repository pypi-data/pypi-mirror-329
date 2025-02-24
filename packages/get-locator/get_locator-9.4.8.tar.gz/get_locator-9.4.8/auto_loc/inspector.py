# auto_loc/inspector.py

import time
import pyperclip
import selenium
from selenium import webdriver
from selenium.common import StaleElementReferenceException, JavascriptException
from auto_loc.locators import get_xpath, get_css_selector
from auto_loc.utils import highlight_element, save_locators_to_json
from pynput import keyboard

class WebInspector:
    def __init__(self, browser="chrome", headless=False, test_attributes: list=None):
        self.test_attributes = test_attributes
        self.options = webdriver.ChromeOptions()
        if headless:
            self.options.add_argument("--headless")
        if browser == 'chrome':
            self.driver = webdriver.Chrome(options=self.options)
        else:
            raise ValueError("Currently only Chrome is supported")
        self.last_element = None
        self.exit_flag = False
        self.current_url = None

    def start(self, url):
        self.driver.get(url)
        self.current_url = url
        print(f"Открыл страницу {url}")
        print("Нажмите 'q' для выхода.")
        self._prevent_new_windows()
        self._inspect_page()

    def _prevent_new_windows(self):
        self.driver.execute_script("""
            function setupClickHandlers() {
                document.addEventListener('click', function(event) {
                    let element = event.target;

                    if (element.tagName === 'A') {
                        if (event.shiftKey) {
                            // Shift + клик – открываем ссылку В ТОМ ЖЕ ОКНЕ вручную
                            event.preventDefault(); // Блокируем стандартное открытие
                            window.location.href = element.href; // Открываем в текущем окне
                        } else {
                            // Обычный клик – предотвращаем переход и выводим локатор
                            event.preventDefault();
                            window.element_path = element; // Сохраняем элемент для обработки
                            console.log("Локатор ссылки:", element.outerHTML);
                        }
                    } else {
                        // Для других элементов только сохраняем путь без предотвращения клика
                        window.element_path = element;
                    }
                }, true);
            }

            setupClickHandlers();
        """)

    def _inspect_page(self):
        print("Инспектор запущен. Одинарный клик — генерация локатора, Shift + клик — стандартное взаимодействие.")
        self.driver.execute_script("""
            document.addEventListener('click', function(event) {
                if (!event.shiftKey) {
                    let element = event.target;
                    window.element_path = element;
                    event.preventDefault();
                    event.stopPropagation();
                }
            }, true);
        """)
        listener = keyboard.Listener(on_press=self._on_key_press)
        listener.start()
        retry_count = 0
        max_retries = 2
        while not self.exit_flag:
            try:
                self._check_url_change()
                element = self.driver.execute_script("return window.element_path;")
                if element and element != self.last_element:
                    self.last_element = element
                    self._highlight_and_generate_locator(element, self.test_attributes)
                    retry_count = 0
                    self.driver.execute_script("window.element_path = null;")
            except selenium.common.exceptions.StaleElementReferenceException:
                retry_count += 1
                if retry_count >= max_retries:
                    retry_count = 0
                    self.driver.execute_script("window.element_path = null;")
                    self.last_element = None
            except selenium.common.exceptions.JavascriptException:
                retry_count += 1
                if retry_count >= max_retries:
                    retry_count = 0
                    self.driver.execute_script("window.element_path = null;")
                    self.last_element = None
            except selenium.common.exceptions.WebDriverException:
                print("Сбой WebDriver, обновляем контекст страницы.")
                self.last_element = None
            except Exception:
                retry_count += 1
                if retry_count >= max_retries:
                    retry_count = 0
                    self.driver.execute_script("window.element_path = null;")
                    self.last_element = None
            time.sleep(0.5)
        listener.stop()

    def _check_url_change(self):
        current_url = self.driver.current_url
        if current_url != self.current_url:
            print(f"URL изменился на {current_url}")
            self.current_url = current_url
            self.driver.execute_script("window.element_path = null;")  # Сбрасываем выбранный элемент
            self._prevent_new_windows()  # Повторная установка обработчиков кликов
            time.sleep(1)  # Ожидание, чтобы новая страница успела загрузиться

    def _highlight_and_generate_locator(self, element, test_attributes):
        try:
            if not self._is_element_stale(element):
                highlight_element(self.driver, element)
                xpath = get_xpath(self.driver, element, test_attributes)
                css_selector = get_css_selector(self.driver, element, test_attributes)
                print(f"\nXPATH локатор: {xpath}")
                print(f"CSS локатор: {css_selector}")
                pyperclip.copy(xpath)
                print("XPATH локатор скопирован в буфер обмена!")
                save_locators_to_json(xpath, css_selector)
            else:
                print("Элемент устарел. Повторный поиск элемента.")
        except StaleElementReferenceException:
            print("Ошибка: Элемент устарел и недоступен. Попробуйте кликнуть снова.")
        except JavascriptException as e:
            print(f"Ошибка JavaScript: {e}")

    def _is_element_stale(self, element):
        try:
            element.is_enabled()
            return False
        except StaleElementReferenceException:
            return True

    def _on_key_press(self, key):
        try:
            if key.char == 'q':
                self._set_exit_flag()
                print("\nExit flag set to True.")
        except AttributeError:
            pass

    def _set_exit_flag(self):
        print("\nВыход из инспектора...")
        self.exit_flag = True

    def quit(self):
        self.driver.quit()

if __name__ == "__main__":
    list_attributes = ["data-test-id", "data-e2e", "test-id"]
    url = "https://3d4medical.com/"
    inspector = WebInspector(test_attributes=list_attributes)
    inspector.start(url)
    inspector.quit()
