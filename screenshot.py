from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from time import sleep
import tempfile

class ScreenShot:

    def __init__(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.opts = FirefoxOptions()
        self.opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=self.opts)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, 768)

    def __del__(self):
        self.driver.quit()

    def scrape_website(self, website):
        self.driver.get(website)
        sleep(1.5)
        height = 0
        try:
            max_height = self.driver.execute_script("return document.body.scrollHeight")
        except:
            print("error")
            max_height = 0
        num = 0

        while(height <= max_height):
            self.driver.execute_script(f"window.scrollTo(0, {height})")
            self.driver.get_screenshot_as_file(f"{self.temp_dir.name}/screenshot{num}.png")
            num += 1
            height += 768
        
        return [f"{self.temp_dir.name}/screenshot{i}.png" for i in range(0, num)] 