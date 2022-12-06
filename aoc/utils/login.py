import os

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from aoc.utils import prep


def get_puzzle_input(day, year=2021):
    from selenium import webdriver

    login_address = 'https://adventofcode.com/auth/github'
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    try:
        driver.get(login_address)

        login_box = driver.find_element(by=By.ID, value='login_field')
        password_box = driver.find_element(by=By.ID, value='password')

        login_box.send_keys(os.environ["GIT_USERNAME"])
        password_box.send_keys(os.environ["GIT_PASSWORD"])

        password_box.submit()

        # wait for oauth redirect
        wait = WebDriverWait(driver, 10)
        wait.until(EC.title_contains("Advent"))

        driver.get(f"https://adventofcode.com/{year}/day/{day}/input")
        input_content = driver.find_element(by=By.TAG_NAME, value="pre")

        text = input_content.text
    finally:
        driver.quit()

    return text


if __name__ == '__main__':
    day_of = 17
    input_text = get_puzzle_input(day_of)
    prep.write_puzzle_input(day_of, input_text)
    print(input_text)
