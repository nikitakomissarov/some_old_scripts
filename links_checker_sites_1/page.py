from selenium import webdriver

class Page:
    def __init__(self, url):
        self.url = url

    def get_driver(self):
        driver = webdriver.Chrome(executable_path=r"C:\Users\big shot\chromedriver\chromedriver.exe") #Указать локальный путь к драйверу на компе
        driver.get(self.url)
        return driver

