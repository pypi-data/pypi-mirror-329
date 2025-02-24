import json
import time

def highlight_element(driver, element, duration=1):
    """Подсветка выбранного элемента на странице с помощью JavaScript."""
    original_style = element.get_attribute('style')
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, "border: 3px solid red;")
    time.sleep(duration)  # Подсвечиваем элемент на указанное время
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_style)

def save_locators_to_json(xpath, css_selector, file_name="locators.json"):
    locators = {
        "xpath": xpath,
        "css_selector": css_selector
    }
    with open(file_name, "a") as file:
        json.dump(locators, file)
        file.write("\n")
