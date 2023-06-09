'''
Author: psg4220
Version: 0.1 Pre-alpha

NOTE: THIS IS FOR TESTING AND EDUCATIONAL PURPOSES ONLY, I AM NOT RESPONSIBLE FOR ANYONE WHO MISUSES MY SCRIPT.
'''

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth


class AutoAIMS:

    def __init__(self):
        self.options = Options()
        self.options.add_argument("start-maximized")

        # Chrome is controlled by automated test software
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=self.options)

        # Selenium Stealth settings
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        self.driver.get("https://cituweb.pinnacle.com.ph/aims/students/")

        '''
        self.menu is the menu bar in that website. These are the following menus:

        0 = Section Offering
        1 = Profile
        2 = Registration
        3 = Grades
        4 = Account
        5 = Calendar
        6 = Faculty Evaluation
        7 = Password
        8 = Schedule
        9 = Curriculum/Evaluation
        10 = Announcement
        11 = Student HandBook

        '''
        self.menu = []

    def login(self, username, password):
        """

        :param username: University ID of the user.
        :param password: a password, duh!

        Logs in to CIT-U's AIMS

        """

        user, pwd = self.driver.find_element(By.NAME, "username"), self.driver.find_element(By.NAME, "password")
        user.send_keys(username)
        pwd.send_keys(password)
        pwd.send_keys(Keys.ENTER)

        # Menu
        self.menu = self.driver.find_elements(By.XPATH, "//div[@class='row aims-menu']//a")

    def automate_faculty_evaluation(self):
        '''

        Cannot make a script simply because the faculty evaluation is not open yet
        or I don't have the source code of the faculty evaluation when its open

        TODO: Find out how the faculty evaluation works if it is open

        '''
        ...
