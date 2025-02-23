import re
from venv import logger

import pyperclip
from selenium.webdriver.common.by import By


def get_xpath(driver, element, test_attributes):
    """Генерация короткого XPATH для элемента с приоритетом поиска по id, тексту, name и другим атрибутам, а также выводом placeholder."""
    first_tag = element.tag_name.lower()
    if first_tag == "svg" or len(first_tag) < 3 or first_tag == "path":
        tag = "*"
    else:
        tag = first_tag

    def is_dynamic_attribute(value):
        # Проверка на динамически сгенерированные атрибуты, например id со случайными числами
        return value.isdigit() or re.match(r".*-\d+", value)

    def generate_primary_xpath():

        def add_index_if_needed(xpath, paragraph: bool = False):
            siblings = driver.find_elements(By.XPATH, xpath)
            if len(siblings) > 1:
                index = siblings.index(element) + 1
                return f"{xpath}[{index}]"
            if paragraph:
                new_path = xpath + "/p"
                elem = driver.find_elements(By.XPATH, new_path)
                if len(elem) > 1:
                    index = elem.index(element) + 1
                    return f"{new_path}[{index}]"
                elif driver.find_element(By.XPATH, xpath+"/child::div").text:
                    return xpath+"/child::div"
                elif driver.find_element(By.XPATH, xpath).text:
                    return xpath
                return new_path
            else:
                return xpath

        # Priority 0: Search by test attributes
        primary_xpath = None
        for attr in test_attributes:
            attr_value = element.get_attribute(attr)
            if attr_value:
                return add_index_if_needed(f"//{tag}[@{attr}='{attr_value}']")

        if not primary_xpath:
            # Priority 1: Search by id
            element_id = element.get_attribute("id")
            if element_id and not is_dynamic_attribute(element_id):
                return add_index_if_needed(f"//{tag}[@id='{element_id}']")
            else:
                # Priority 2: Search by text
                text = element.text.strip()
                check_text = ["title", "lower", "upper", "capitalize"]
                if text and len(text) < 50:
                    for check in check_text:
                        text_new = getattr(text, check)()
                        try:
                            if driver.find_element(By.XPATH, f"//{tag}[text()=\"{text_new}\"]").text == text:
                                text = text_new
                                break
                        except Exception:
                            logger.info(f"Text check failed: {check}")
                    return add_index_if_needed(f"//{tag}[text()=\"{text}\"]")
                else:
                    # Priority 3: Search by name
                    element_name = element.get_attribute("name")
                    if element_name:
                        return add_index_if_needed(f"//{tag}[@name='{element_name}']")
                    else:
                        # Priority 4: Search by classes
                        element_class = element.get_attribute("class")
                        classes = ".".join(element_class.split())
                        paragraph = False
                        if element_class:
                            return add_index_if_needed(f"//{tag}[contains(@class, '{classes}')]")
                        else:
                            text = element.text.strip()
                            if text and len(text) > 50:
                                paragraph = True
                            # Search in parent elements if the current element does not have the class attribute
                            parent = element.find_element(By.XPATH, "..")
                            while parent:
                                parent_id = parent.get_attribute("id")
                                if parent_id and not is_dynamic_attribute(parent_id):
                                    return add_index_if_needed(f"//{parent.tag_name.lower()}[@id='{parent_id}']",
                                                               paragraph)
                                parent_class = parent.get_attribute("class")
                                if parent_class:
                                    parent_classes = ".".join(parent_class.split())
                                    return add_index_if_needed(
                                        f"//{parent.tag_name.lower()}[contains(@class, '{parent_classes}')]")
                                parent = parent.find_element(By.XPATH, "..")
                            return add_index_if_needed(f"//{tag}[contains(@class, '{classes}')]")

    primary_xpath = generate_primary_xpath()

    # Placeholder locator, if present
    placeholder = element.get_attribute("placeholder")
    placeholder_xpath = f"//{tag}[@placeholder='{placeholder}']" if placeholder else ""

    return primary_xpath + ("\n" + "Placeholder: " + placeholder_xpath if placeholder_xpath else "")


def get_css_selector(driver, element, test_attributes):
    def add_index_if_needed(css_selector):
        siblings = driver.find_elements(By.CSS_SELECTOR, css_selector)
        if len(siblings) > 1:
            index = siblings.index(element) + 1
            return f"{css_selector}:nth-of-type({index})"
        return css_selector

    tag = element.tag_name.lower()

    def is_dynamic_attribute(value):
        # Проверка на динамически сгенерированные атрибуты, например id со случайными числами
        return value.isdigit() or re.match(r".*-\d+", value)

    # Priority 0: Search by test attributes
    primary_css = None
    for attr in test_attributes:
        attr_value = element.get_attribute(attr)
        if attr_value:
            primary_css = f"{tag}[{attr}='{attr_value}']"
            break

    if not primary_css:
        # Priority 1: Search by id
        element_id = element.get_attribute("id")
        if element_id and not is_dynamic_attribute(element_id):
            primary_css = f"{tag}#{element_id}"
        else:
            # Priority 2: Search by name
            element_name = element.get_attribute("name")
            if element_name:
                primary_css = f"{tag}[name='{element_name}']"
            else:
                # Priority 3: Search by classes
                element_class = element.get_attribute("class")
                if element_class:
                    classes = ".".join(element_class.split())
                    primary_css = f"{tag}.{classes}"
                else:
                    # Priority 4: Indexing among tags of the same type
                    primary_css = f"{tag}"

    primary_css = add_index_if_needed(primary_css)

    # Placeholder locator, if present
    placeholder = element.get_attribute("placeholder")
    placeholder_css = f"{tag}[placeholder='{placeholder}']" if placeholder else ""

    # Search in parent elements if the current element does not have the class attribute
    element_class = element.get_attribute("class")
    if not element_class:
        parent = element.find_element(By.XPATH, "..")
        while parent:
            parent_id = parent.get_attribute("id")
            if parent_id and not is_dynamic_attribute(parent_id):
                return add_index_if_needed(f"{parent.tag_name.lower()}#{parent_id}")
            parent_class = parent.get_attribute("class")
            if parent_class:
                parent_classes = ".".join(parent_class.split())
                return add_index_if_needed(f"{parent.tag_name.lower()}.{parent_classes}")
            parent = parent.find_element(By.XPATH, "..")

    return primary_css + ("\n" + "Placeholder: " + placeholder_css if placeholder_css else "")


def copy_to_clipboard(locator):
    """Копирование локатора в буфер обмена."""
    pyperclip.copy(locator)
    print("Локатор скопирован в буфер обмена!")
