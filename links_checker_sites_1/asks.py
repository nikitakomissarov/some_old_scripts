import requests
from requests.exceptions import MissingSchema
from requests.exceptions import InvalidSchema
from requests.exceptions import ConnectionError
from selenium.webdriver.common.by import By


class Links:

    def __init__(self, browser):
        self.browser = browser

    def requesting(self, key, clean_links=None, invalid_links=None, foreign_links=None, wrong_links=None):
        try:
            if clean_links is None:
                clean_links = list()
            if invalid_links is None:
                invalid_links = list()
            if foreign_links is None:
                foreign_links = list()
            if wrong_links is None:
                wrong_links = list()

            burger_bar_links = self.browser.find_elements(By.XPATH, "//a")

            for link in burger_bar_links:
                check = link.get_attribute('href')

                if check not in clean_links and check not in foreign_links:
                    try:
                        a = requests.head(link.get_attribute('href')).status_code == 200
                        cleanlink = link.get_attribute('href')
                        print(f'LINK VALID {cleanlink}')
                        # print("Link is Valid:", cleanlink)
                        if cleanlink.startswith(key) and cleanlink not in clean_links:
                            clean_links.append(cleanlink)
                        else:
                            foreign_links.append(cleanlink)
                            continue

                    except InvalidSchema:
                        wrong_link = link.get_attribute('href'), link.get_attribute('outerHTML'), self.browser.current_url
                        if wrong_link not in wrong_links:
                            wrong_links.append(wrong_link)
                            print(f'InvalidSchema {wrong_link}')

                    except MissingSchema:
                        wrong_link = link.get_attribute('href'), link.get_attribute('outerHTML'), self.browser.current_url
                        if wrong_link not in wrong_links:
                            wrong_links.append(wrong_link)
                            print(f'InvalidSchema {wrong_link}')

                    except ConnectionError:
                        invalidlink = link.get_attribute('href'), link.get_attribute('outerHTML'), self.browser.current_url
                        if invalidlink not in invalid_links:
                            invalid_links.append(invalidlink)
                            print(f'ConnectionError, LINK IS INVALID:" {invalidlink}')
                else:
                    continue
        finally:
            self.browser.quit()
        return clean_links, invalid_links, foreign_links, wrong_links


