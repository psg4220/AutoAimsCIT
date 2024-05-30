"""
Author: psg4220
Version: 0.1 Pre-alpha

NOTE: THIS IS FOR TESTING AND EDUCATIONAL PURPOSES ONLY, I AM NOT RESPONSIBLE FOR ANYONE WHO MISUSES MY SCRIPT.
"""
import enum
import logging
import time
from telnetlib import EC

from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import CONSTANTS
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium_stealth import stealth


class Semester(enum.Enum):
    FIRST = "A"
    SECOND = "B"
    THIRD = "D"
    SUMMER = "C"


class Rating(enum.Enum):
    OUTSTANDING = 0
    VERY_GOOD = 1
    GOOD = 2
    NEEDS_IMPROVEMENT = 3
    POOR = 4


class AutoAIMS:

    def __init__(self, show_browser=False):

        logging.basicConfig(level=logging.DEBUG)

        try:
            self.options = webdriver.ChromeOptions()
            # # Hide or maximize window
            if not show_browser:
                self.options.add_argument("--headless" if CONSTANTS.hide_window else "--start-maximized")

            # Chrome is controlled by automated test software
            self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
            self.driver.get("http://www.python.org")
            logging.debug("add_experimental_option method set is complete")

            # Selenium Stealth settings
            stealth(self.driver,
                    user_agent=CONSTANTS.useragent,
                    languages=CONSTANTS.languages,
                    vendor=CONSTANTS.vendor,
                    platform=CONSTANTS.platform,
                    webgl_vendor=CONSTANTS.webgl_vendor,
                    renderer=CONSTANTS.renderer,
                    fix_hairline=CONSTANTS.fix_hairline,
                    run_on_insecure_origins=CONSTANTS.run_on_insecure_origins
                    )
            self.driver.get("https://cituweb.pinnacle.com.ph/aims/students/")
            self.menu = []

        except NoSuchDriverException:
            logging.error("Web driver was not found | Only Chrome driver is supported")
        except WebDriverException:
            logging.error("Something is wrong with the Web Driver")
        finally:
            logging.info("__init__ of AutoAIMS class is finished")

    def login(self, username, password):
        """
        Logs in to CIT-U's AIMS
        :param username: University ID of the user.
        :param password: a password, duh!
        """

        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        logging.debug("Successfully found the element, inserting username and password")

        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        logging.debug("ENTER key was pressed")

        # Menu
        self.menu = self.driver.find_elements(By.XPATH, "//div[@class='row aims-menu']//a")
        logging.debug("Menu was successfully extracted to self.menu")

    def automate_faculty_evaluation(self, school_year: str = "2324",
                                    semester: Semester = Semester.SECOND,
                                    rating: Rating = Rating.GOOD,
                                    meet_again=True):
        """
        Cannot make a script simply because the faculty evaluation is not open yet
        or I don't have the source code of the faculty evaluation when it's open
        TODO: Find out how the faculty evaluation works if it is open
        """
        global radio_buttons
        try:
            # Locate the elements matching the provided XPath
            elements = self.driver.find_elements(By.XPATH, "//span[@class='aimsMenu ']//span[@class='notActiveMenu']")

            # Iterate through the elements to find the one with the correct text
            for element in elements:
                if element.text.strip() == "Faculty Evaluation":
                    element.click()
                    logging.info("Clicked on Faculty Evaluation")
                    break

            # Add a delay to wait for the page to load if necessary
            self.driver.implicitly_wait(10)  # Adjust the wait time as needed

            # Select the dropdown options
            # Select the "SY" dropdown and choose the option with value '2324'
            sy_select = Select(self.driver.find_element(By.NAME, "cboSY"))
            sy_select.select_by_value(school_year)

            # Select the "Semester" dropdown and choose the option with value 'A'
            sem_select = Select(self.driver.find_element(By.NAME, "cboSem"))
            sem_select.select_by_value(semester.value)

            # Locate the table containing the course codes
            table = self.driver.find_element(By.XPATH, "//table[@class='dbtable table table-bordered']")

            # Find all clickable course codes within the table
            clickable_courses = table.find_elements(By.XPATH, ".//td[@class='regu']/a")

            # Handle each clickable course
            for course in clickable_courses:
                # Click on the course
                course.click()

                # Handle pop-up window
                # Get the current window handle (main window)
                main_window_handle = self.driver.current_window_handle

                # Get all window handles
                all_window_handles = self.driver.window_handles

                # Switch to the new window
                for window_handle in all_window_handles:
                    if window_handle != main_window_handle:
                        self.driver.switch_to.window(window_handle)
                        break

                # Now you are in the pop-up window, perform actions here as needed

                try:
                    # Locate the ul element by its ID
                    ul_element = self.driver.find_element(By.ID, "evalform-titles")

                    # Find all li elements inside the ul
                    li_elements = ul_element.find_elements(By.XPATH, ".//li")

                    # Iterate through each li element
                    for i, li in enumerate(li_elements):
                        # Click on the div element
                        li.click()

                        # Construct the CSS selector for the radio buttons based on the current index
                        css_selector = f"input[type='radio'][catCode='C0{264 + i}']"

                        # Find the radio buttons using the CSS selector
                        radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, css_selector)

                        # Click the radio button with the text "Good"
                        for radio_index, radio_button in enumerate(radio_buttons):
                            if radio_index % 5 == rating.value:
                                radio_button.click()

                        # Add a delay if necessary to wait for the page to load after clicking
                    if meet_again:
                        radio_buttons[len(radio_buttons) - 2].click()
                    else:
                        radio_buttons[len(radio_buttons) - 1].click()

                    text_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text']")
                    for text_input in text_inputs:
                        text_input.clear()  # Clear any existing text
                        text_input.send_keys("None")  # Input the word "None"

                    # Click finish button
                    button = self.driver.find_element(By.CSS_SELECTOR, "input[type='button'].finish")
                    button.click()

                    WebDriverWait(self.driver, 10).until(EC.alert_is_present())

                    alert = self.driver.switch_to.alert
                    alert.accept()

                    WebDriverWait(self.driver, 10).until(EC.alert_is_present())

                    alert = self.driver.switch_to.alert
                    alert.accept()

                except Exception as e:
                    logging.error(f"An error occurred: {e}")

                self.driver.close()

                # Switch back to the main window
                self.driver.switch_to.window(main_window_handle)

        except Exception as e:
            logging.error(f"An error occurred: {e}")

    # Feel free to add more methods

    def wait_for_popup_window(self, main_window_handle, timeout=10):
        """
        Wait for a pop-up window to appear and return its handle
        """
        popup_window_handle = None
        wait = WebDriverWait(self.driver, timeout)

        # Wait for a new window handle to appear
        wait.until(EC.new_window_is_opened)

        # Get all window handles
        all_window_handles = self.driver.window_handles

        # Find the handle of the new window (excluding the main window handle)
        for window_handle in all_window_handles:
            if window_handle != main_window_handle:
                popup_window_handle = window_handle
                break

        return popup_window_handle
