from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os


class User:
    def __init__(self, username: str, password: str, headless: bool = True) -> None:
        self.__username = username
        self.__password = password
        # create a new Chrome session
        self.__headless = headless
        self.__driver = None
    def __del__(self) -> None:
        if self.__driver is not None:
            self.__driver.quit()

    def login(self) -> None:
        options = webdriver.ChromeOptions()
        if self.__headless:
            options.add_argument("--headless")
            options.add_argument("--window-size=1920,1080")
        if os.path.exists("/.dockerenv"):
            driver = webdriver.Remote(
                command_executor="http://localhost:4444/wd/hub",
                options=options,
            )
        else:
            driver = webdriver.Chrome(options=options)
        self.__driver = driver
        driver.get("https://scrsprd.zju.edu.cn/psp/CSPRD/?cmd=login&languageCd=ENG&&accttp=zju")

        # wait for the username input to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(self.__username)
        driver.find_element(By.ID, "password").send_keys(self.__password)
        driver.find_element(By.ID, "dl").click()

    def grade(self, choice=1) -> None:
        if self.__driver is None:
            self.login()
        
        driver = self.__driver
        driver.get("https://scrsprd.zju.edu.cn/psc/CSPRD_newwin/EMPLOYEE/HRMS/c/SSR_STUDENT_ACAD_REC_FL.SSR_ACAD_REC_FL.GBL")

        choices = [
            "win1sidedivSCC_NAV_TAB_row$0",
            "win1sidedivSCC_NAV_TAB_row$1",
            "win1sidedivSCC_NAV_TAB_row$2",
            "win1sidedivSCC_NAV_TAB_row$3",
        ]

        # enter the selected page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, choices[choice-1]))
        ).click()

        if choice == 2:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".ps_grid-row.psc_rowact"))
            )
            choices = driver.find_elements(By.CSS_SELECTOR, ".ps_grid-row.psc_rowact")
            choices[0].click()

            # get cources
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "TERM_CLASSES$0_row_0"))
            )
            cources = driver.find_elements(By.CSS_SELECTOR, "[id^=TERM_CLASSES]")
            for i in range(len(cources)):
                items = cources[i].find_elements(By.CLASS_NAME, "ps_grid-cell")
                cources[i] = {
                    "class": items[0].text,
                    "description": items[1].text,
                    "units": items[2].text,
                    "grading": items[3].text,
                    "grade": items[4].text,
                    "grade_points": items[5].text
                }
            return cources
        elif choice == 3 or choice == 4:
            return driver.execute_script("return document.documentElement.outerHTML")
